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
from itertools import combinations, combinations_with_replacement
from utils import check_solution, clean_word, get_features, get_min_mask
from stanford_corenlp import tokenize_sentences



types = ['return', 'mapping', 'valid', 'reduce']
# types = ['return', 'mapping', 'valid', 'reduce', 'possibilities', 'types']
# types = ['I']

def get_type(sentence, translations, code, method):
    '''
    get the sentence type according to the code and method
    
    :param sentence:
    :param translations:
    :param code:
    :param method:
    '''
    if not code:
        return 'O'
    if method[0]:
        m = re.match(r'\s*def\s+(.+)\(.*\):\s*', method[0])
        sentence_type = clean_word(m.group(1))
        if sentence_type in types:
            return sentence_type
    if len(code) == 1:
        codewords = nltk.word_tokenize(code[0])
        sentence_type = clean_word(codewords[0])
        if sentence_type in types:
            return sentence_type
        if sentence_type == 'def' and clean_word(codewords[1]) in types:
            return clean_word(codewords[1])
    else:
        codewords = nltk.word_tokenize(code[-1])
        if not method[0] and codewords[0] == 'return':
            return 'return'
#     print(method)
#     print(code)
    return 'O'

def label_sentence(sentence,translations,code,method):
    '''
    label should be according to sentence type
    between first and last translated words, else 'O'

    :param sentence:
    :param translations:
    :param code:
    :param symbol:
    :returns: labeled sentence    
    '''
#     sentwords = nltk.word_tokenize(sentence.lower())
    sentwords = tokenize_sentences(sentence.lower())[0]
    pos = zip(*nltk.pos_tag(sentwords))[1]
    N = len(sentwords)
    features = get_features(sentence)
    symbol = get_type(sentence, translations, code, method)
    labels = ['O'] * N
    relevantwords = set()
    for translation,codeline in zip(translations,code):
#         codewords = nltk.word_tokenize(codeline)
        transwords = nltk.word_tokenize(translation)
#         if not codewords:
#             continue
        relevantwords.update(set(sentwords) & set(transwords) - set(string.punctuation))
#         relevantwords += [word for word in transwords if word not in string.punctuation]
    mask = get_min_mask(sentwords,relevantwords)
    labels = [ symbol if mask[i] else labels[i] for i in range(N)]
#         index = mask.index(1)
#         labels[index] = 'B'+symbol
    return zip(sentwords,pos,features, labels)

def label_problem(indir, outdir, fname):
    '''
    label each sentence of the given problem
    
    :param indir: path to the problem
    :param outdir: path to write the labeled problem
    :param fname: problem name
    '''
    with open(os.path.join(indir,fname),'r') as f:
        problem = f.read()
    parse = parse_problem(problem)
    sentence_labels = []
    for sentence_parse in parse['sentences']:
        sentence = sentence_parse['sentence']
#         print(sentence)
        translations = sentence_parse['translations']
        code = sentence_parse['code']
        method = sentence_parse['method']
#         if not code:
#             continue
#         print(symbol)
        labels = label_sentence(sentence, translations, code, method)
        sentence_labels.append(labels)
    fileBase, fileExtension = os.path.splitext(fname)
    with open(os.path.join(outdir,fileBase+'.label'),'w') as f:
        f.write('\n\n'.join(['\n'.join(['\t'.join(label) for label in labels]) for labels in sentence_labels]))

def build_train(indir, outdir):
    '''
    build train database by labeling each problem in indir
    
    :param indir: path to problems to label
    :param outdir: path to write labeled problems
    '''
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    os.mkdir(outdir)
    for fname in sorted(os.listdir(indir)):
        if not fname.endswith('.py'):
            continue
        print(fname)
        label_problem(indir, outdir, fname)

def get_probable_sentence_type(sentences_json, sentence, n):
    '''
    get the most probable sentence type for the given sentence
    
    :param sentences_json:
    :param sentence:
    :param n: number of possible sentences for each type
    '''
    possible_types = []
    sentind = sentences_json.index(sentence)
    for sentence_type in types:
        sentprobs = get_sentences_probabilities(sentences_json, sentence_type, n)
        for sentprob in sentprobs:
            if sentind == sentprob[-1]:
                possible_types.append((sentprob[0], sentence_type))
    if not possible_types:
        return None
    possible_types = sorted(possible_types, reverse=True)[0]
    return possible_types[-1]

def get_sentences_probabilities(problem_json, symbol, n=None):
    '''
    get probability for the given symbol, for each of the sentence in the problem    
    
    :param problem_json:
    :param symbol:
    :param n: number of possible sentences for each type
    '''
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
        sentprobs.append((sentprob,important,i))
    sentprobs = sorted(sentprobs,reverse = True)
    return sentprobs[:n]

def get_expected_sents(problem_json, symbol): 
    '''
    get the actual sentences for the given symbol
    
    :param problem_json:
    :param symbol:
    '''
    expected_sents = []
    for i,sentence in enumerate(problem_json):
        for line in sentence:
            if line['label'] == symbol:
                expected_sents.append(i)
    return expected_sents

def get_expected_type(sentence):
    '''
    get the actual type for the given sentence
    
    :param sentence:
    '''
    for line in sentence:
        if line['label'] in types:
            return line['label']
    
# def check_problem(json_dir,fname,n):
#     '''
#     check if n most probable sentences contain all the sentences of a certain type, for all types
#       
#     :param json_dir:
#     :param fname:
#     :param n: number of possible sentences for each type
#     '''
#     with open(os.path.join(json_dir,fname),'r') as inputjson:
#         problem_json = json.load(inputjson)
#     results = []
#     for sentence_type in types:
#         sentprobs = get_sentences_probabilities(problem_json,sentence_type)
#         probable_sents = zip(*sentprobs)[-1][:n]
#         expected_sents = get_expected_sents(problem_json,sentence_type)
#         result = set(expected_sents).issubset(set(probable_sents))
# #         result = all([not important for (sentprob,i,important) in sentprobs[n:]])
#         if not result:
#             logger.logging.info(fname)
#             logger.logging.info(sentence_type)
#             logger.logging.info(expected_sents)            
#             logger.logging.info(sentprobs)
#         results.append(result)
#     return results

def check_problem(json_dir,fname,n):
#         check if n most probable sentences contain all important sentences
    with open(os.path.join(json_dir,fname),'r') as inputjson:
        problem_json = json.load(inputjson)
    results = []
    for sentence in problem_json:
        expected_type = get_expected_type(sentence)
        expected_type_sentprobs = get_sentences_probabilities(problem_json,expected_type)
        probable_type = get_probable_sentence_type(problem_json, sentence, n)
        probable_type_sentprobs = get_sentences_probabilities(problem_json,probable_type)
        result = not expected_type or expected_type == probable_type
        if not result:
            logger.logging.info(fname)
            logger.logging.info(problem_json.index(sentence))
            logger.logging.info(expected_type)
            logger.logging.info(expected_type_sentprobs)
            logger.logging.info(probable_type)
            logger.logging.info(probable_type_sentprobs)
        results.append(result)
    return results

def calc_score(json_dir,n=4, problem_dir=None):
    '''
    calculate how many problems pass the check in the given path

    :param json_dir: path to the problems
    :param n: number of possible sentences for each label 
    :param problem_dir: given to allow checking whether a problem has a solution 
    '''
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


def main():
    indir = os.path.join('res', 'text&code5')
    indir = os.path.join('res', 'text&code6')
    train_dir = os.path.join(indir, 'sentence_train')
    fname = 'ChocolateBar.py'
#     label_problem(indir, train_dir, fname)
#     build_train(indir, train_dir)

    test_indir = os.path.join('res', 'problems_test')
    test_dir = os.path.join(test_indir, 'sentence_test')
#     build_train(test_indir, test_dir)

    outdir = os.path.join(indir, 'sentence_json')
#     CRF.test(train_dir, outdir)

    test_outdir = os.path.join(test_indir, 'sentence_json')
#     CRF.test(train_dir, test_outdir, test_dir)

    n = 1
    print(calc_score(outdir, n, indir))

    fname = 'AverageAverage.label'
    fname = 'ChocolateBar.label'
    fname = 'CompetitionStatistics.label'
#     fname = 'ChristmasTreeDecorationDiv2.label'
#     fname = 'Elections.label'
#     fname = 'FarFromPrimes.label'
#     fname = 'LittleElephantAndBallsAgain.label'
#     print(check_problem(outdir, fname, n))


if __name__ == '__main__':
    main()
