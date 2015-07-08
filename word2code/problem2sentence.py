'''
Created on Apr 6, 2015

@author: jordan
'''
#     extract significant phrases from problem
import nltk
from problem_parser import parse_problem
import os
import subprocess
import string
import re
import json
import ast
import CRF
import shutil
import logger
from codeline_gen_dep import clean_codeline

# get minimal continuous subset containing all relevant words
# example:
#         sentence words: ["hello", "world", ",", "how", "are", "you", "?"]
#         relevant words: ["world", "are"]
#         smallest csubset: ["world", ",", "how", "are"]
def get_min_mask(sentwords,relevantwords):
    relevantset = set(relevantwords)
    N = len(sentwords)
    mask = [0] * N
    for i in range(N):
        for j in range(N-i):
            if relevantset.issubset(sentwords[j:j+i]):
                mask[j:j+i] = [1] * i
                return mask
    return [1] * N

types = ['return', 'mapping', 'valid', 'reduce', 'possibilities', 'types']
# types = ['I']

def clean_codeword(codeword):
    return re.sub(r'\d?$', '', codeword)

def get_type(sentence, translations, code, method):
    if method[0]:
        m = re.match(r'\s*def\s+(.+)\(.*\):\s*', method[0])
        sentence_type = clean_codeword(m.group(1))
        if sentence_type in types:
            return sentence_type
    if len(code) == 1:
        codewords = nltk.word_tokenize(code[0])
        sentence_type = clean_codeword(codewords[0])
        if sentence_type in types:
            return sentence_type
        if sentence_type == 'def' and clean_codeword(codewords[1]) in types:
            return clean_codeword(codewords[1])
    else:
        codewords = nltk.word_tokenize(code[-1])
        if codewords[0] == 'return':
            return 'return'
    print(method)
    print(code)
    return None

#     input: sentence, translated code, code
#     output: labeled sentence
#     label should be according to sentence type (mapping 'M', valid 'V', return 'R')
#     between first and last translated words, else 'O'
def label_sentence(sentence,translations,code,symbol):
    sentwords = nltk.word_tokenize(sentence.lower())
    pos = zip(*nltk.pos_tag(sentwords))[1]
    N = len(sentwords)
    labels = ['O'] * N
    for translation,codeline in zip(translations,code):
        codewords = nltk.word_tokenize(codeline)
        transwords = nltk.word_tokenize(translation)
        if not codewords:
            continue
#         symbol = codewords[0][0].upper()
#         symbol = 'I'
        relevantwords = list(set(sentwords) & set(transwords))
        relevantwords = [word for word in relevantwords if word not in string.punctuation]
        mask = get_min_mask(sentwords,relevantwords)
        if 1 not in mask:
            continue
        labels = [ symbol if mask[i] else labels[i] for i in range(N)]
#         index = mask.index(1)
#         labels[index] = 'B'+symbol
    return zip(sentwords,pos,labels)

def build_train(indir, outdir):
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    os.mkdir(outdir)
    for fname in sorted(os.listdir(indir)):
        print(fname)
        with open(os.path.join(indir,fname),'r') as f:
            problem = f.read()
        parse = parse_problem(problem)
        sentence_labels = []
        for sentence_parse in parse['sentences']:
            sentence = sentence_parse['sentence']
            translations = sentence_parse['translations']
            code = sentence_parse['code']
            method = sentence_parse['method']
            if not code:
                continue
            symbol = get_type(sentence, translations, code, method)
            if not symbol:
                continue               
            labels = label_sentence(sentence, translations, code, symbol)
            sentence_labels.append(labels)
        fileBase, fileExtension = os.path.splitext(fname)
        with open(os.path.join(outdir,fileBase+'.label'),'w') as f:
            f.write('\n\n'.join(['\n'.join(['\t'.join(label) for label in labels]) for labels in sentence_labels]))


def get_sentences_probabilities(problem_json, symbol):
    sentprobs = []
    for i,sentence in enumerate(problem_json):
        sentprob = 0
        important = False
        for line in sentence:
            if line['label'] == symbol:
                important = True
            probs = {v: k for k, v in ast.literal_eval(line['probs'])}
            if symbol not in probs:
                prob = 0
            else:
                prob = probs[symbol]
            sentprob = prob if sentprob < prob else sentprob
#                 if line['prediction'][1] == 'O':
#                     continue
#                 if line['label'] == line['prediction'][1]:
#                     correct +=1
#                 total += 1
        sentprobs.append((sentprob,i,important))
    return sentprobs

def check_problem(json_dir,fname,n):
#         check if n most probable sentences contain all important sentences
    with open(os.path.join(json_dir,fname),'r') as inputjson:
        problem_json = json.load(inputjson)
    results = []
    for sentence_type in types:
        sentprobs = get_sentences_probabilities(problem_json,sentence_type)
        sentprobs = sorted(sentprobs,reverse = True)
        result = all([not important for (sentprob,i,important) in sentprobs[n:]])
#         if not result:
        logger.logging.info(fname)
        logger.logging.info(sentence_type)            
        logger.logging.info(sentprobs)
        results.append(result)
    return results

def calc_score(json_dir,n=4):
    correct = []
    total = 0
    fnames = sorted(os.listdir(json_dir))
#     for problem in problems_json:
    for fname in fnames:
        results = check_problem(json_dir,fname,n)
        if all(results):
            correct.append(fname)
        total += 1
    print(total)
    print(float(len(correct))/total)
    return correct



if __name__ == '__main__':
#     with open('res/text&code3/AmoebaDivTwo.py') as f:
#         problem = f.read()
#     parse = parse_problem(problem)
#     for sentence_parse in parse['sentences']:
#         sentence = sentence_parse['sentence']
#         translations = sentence_parse['translations']
#         code = sentence_parse['code']
#         print(label_sentence(sentence, translations, code))


    indir = 'res/text&code5/'
    indir = 'res/text&code6'
    train_dir = 'res/sentence_train'
    train_dir = 'res/sentence_train6'
    build_train(indir, train_dir)
 
#     indir = 'res/problems_test/'
#     test_dir = 'res/sentence_test'
#     build_train(indir, test_dir)

#     outdir = 'res/sentence_json'
#     outdir = 'res/sentence_json_small'
    outdir = 'res/sentence_json6'
    CRF.test(train_dir, outdir, features=1)
#     CRF.test(train_dir, outdir, test_dir, features=1)

    n = 1
    print(calc_score(outdir, n))

    fname = 'AverageAverage.label'
#     fname = 'ChristmasTreeDecorationDiv2.label'
#     fname = 'Elections.label'
#     fname = 'FarFromPrimes.label'
#     fname = 'LittleElephantAndBallsAgain.label'
#     print(check_problem(outdir, fname,n))