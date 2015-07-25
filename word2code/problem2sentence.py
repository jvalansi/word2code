'''
Created on Apr 6, 2015

@author: jordan
'''
#     extract significant phrases from problem
import nltk
from problem_parser import parse_problem
import os
import string
import re
import json
import ast
import CRF
import shutil
import logger
from itertools import combinations
from utils import check_solution

# get minimal continuous subset containing all relevant words
# example:
#         sentence words: ["hello", "world", ",", "how", "are", "you", "?"]
#         relevant words: ["world", "are"]
#         smallest csubset: ["world", ",", "how", "are"]
def get_min_mask(sentwords,relevantwords):
    relevantset = set(relevantwords)
    N = len(sentwords)
    mask = [1] * N
    for i,j in combinations(range(N), 2):
        if relevantset.issubset(sentwords[i:j]):
            new_mask = [0] * N
            new_mask[i:j] = [1] * (j-i)
            if sum(new_mask) < sum(mask):
                mask = new_mask
    return mask


types = ['return', 'mapping', 'valid', 'reduce', 'possibilities', 'types']
# types = ['I']

def clean_codeword(codeword):
    return re.sub(r'\d?$', '', codeword)

def get_type(sentence, translations, code, method):
    if not code:
        return None
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

def label_problem(indir, outdir, fname):
    with open(os.path.join(indir,fname),'r') as f:
        problem = f.read()
    parse = parse_problem(problem)
    sentence_labels = []
    for sentence_parse in parse['sentences']:
        sentence = sentence_parse['sentence']
        print(sentence)
        translations = sentence_parse['translations']
        code = sentence_parse['code']
        method = sentence_parse['method']
        if not code:
            continue
        symbol = get_type(sentence, translations, code, method)
        print(symbol)
        if not symbol:
            continue               
        labels = label_sentence(sentence, translations, code, symbol)
        sentence_labels.append(labels)
    fileBase, fileExtension = os.path.splitext(fname)
    with open(os.path.join(outdir,fileBase+'.label'),'w') as f:
        f.write('\n\n'.join(['\n'.join(['\t'.join(label) for label in labels]) for labels in sentence_labels]))

def build_train(indir, outdir):
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    os.mkdir(outdir)
    for fname in sorted(os.listdir(indir)):
        print(fname)
        if not fname.endswith('.py'):
            continue
        label_problem(indir, outdir, fname)

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
        sentprobs.append((sentprob,important,i))
    sentprobs = sorted(sentprobs,reverse = True)
    return sentprobs

def get_expected_sents(problem_json, symbol): 
    expected_sents = []
    for i,sentence in enumerate(problem_json):
        for line in sentence:
            if line['label'] == symbol:
                expected_sents.append(i)
    return expected_sents

def check_problem(json_dir,fname,n):
#         check if n most probable sentences contain all important sentences
    with open(os.path.join(json_dir,fname),'r') as inputjson:
        problem_json = json.load(inputjson)
    results = []
    for sentence_type in types:
        sentprobs = get_sentences_probabilities(problem_json,sentence_type)
        probable_sents = zip(*sentprobs[:n])[-1]
        expected_sents = get_expected_sents(problem_json,sentence_type)
        result = set(expected_sents).issubset(set(probable_sents))
#         result = all([not important for (sentprob,i,important) in sentprobs[n:]])
        if not result:
            logger.logging.info(fname)
            logger.logging.info(sentence_type)            
            logger.logging.info(sentprobs)
        results.append(result)
    return results

def calc_score(json_dir,n=4, problem_dir=None):
    correct = []
    total = 0
    fnames = sorted(os.listdir(json_dir))
#     for problem in problems_json:
    for fname in fnames:
        if problem_dir and not check_solution(os.path.join(problem_dir, re.sub('.label', '.py', fname))):
            continue
        results = check_problem(json_dir,fname,n)
        if all(results):
            correct.append(fname)
        total += 1
    print(total)
    print(float(len(correct))/total)
    return correct



if __name__ == '__main__':

    main_indir = os.path.join('res', 'text&code5')
    main_indir = os.path.join('res', 'text&code6')
    main_train_dir = os.path.join(main_indir, 'sentence_train')
    main_fname = 'ChocolateBar.py'
    label_problem(main_indir, main_train_dir, main_fname)
#     build_train(main_indir, main_train_dir)

#     indir = 'res/problems_test/'
#     test_dir = 'res/sentence_test'
#     build_train(main_indir, main_test_dir)

#     outdir = 'res/sentence_json'
#     outdir = 'res/sentence_json_small'
    main_outdir = os.path.join(main_indir, 'sentence_json')
#     CRF.test(main_train_dir, main_outdir, features=1)
#     CRF.test(main_train_dir, main_outdir, main_test_dir, features=1)

    n = 1
#     print(calc_score(main_outdir, n, main_indir))

    main_fname = 'AverageAverage.label'
    main_fname = 'ChocolateBar.label'
#     fname = 'ChristmasTreeDecorationDiv2.label'
#     fname = 'Elections.label'
#     fname = 'FarFromPrimes.label'
#     fname = 'LittleElephantAndBallsAgain.label'
#     print(check_problem(main_outdir, main_fname,n))