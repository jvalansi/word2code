'''
Created on Apr 2, 2015

@author: jordan
'''

import logging
import logger

import nltk
import re
import os
from problem_parser import parse_problem
import string
import CRF
import json
import ast
import shutil

from matplotlib.pyplot import imshow
from dependency_parser import dep2dict, sentence2dependencies
from operator import indexOf
from utils import is_func, check_solution, get_features
from stanford_corenlp import tokenize_sentences


# mapping = lambda x: x
# valid = lambda x: True
# array = ['input_array','possibilities','types','possibility',]
# primitive = ['j', 'i', 'inf', 'N','element','number','input_int', '0', '1', '2']
# non_callable = set()
# non_relevant = []



types = ['mapping', 'valid', 'reduce']
# types = ['I']

def get_type(codewords):
    '''
    get word type from codewords
    
    :param codewords:
    '''
    if not codewords:
        return ''
    for word_type in types:
        if codewords[0].startswith(word_type):
            return word_type
    print(codewords[0])
    return ''


def label_sentence_by_type(sentence,translations,code):
    '''
    label the sentence for each of the types in each codeline in the code
    
    :param sentence:
    :param translations:
    :param code:
    '''
#     sentwords = nltk.word_tokenize(sentence.lower())
    sentwords = tokenize_sentences(sentence.lower())[0]
    pos = zip(*nltk.pos_tag(sentwords))[1]
    features = get_features(sentence)
    N = len(sentwords)
    labels = ['O'] * N
    for translation,codeline in zip(translations,code):
        codewords = nltk.word_tokenize(codeline)
        transwords = nltk.word_tokenize(translation)
        label = get_type(codewords)
        if not label:
            continue
        if ':' in transwords:
            transwords = transwords[indexOf(transwords, ':')+1:]
            codewords = codewords[indexOf(codewords, ':')+1:]
        if '=' in transwords:
            transwords = transwords[indexOf(transwords, '=')+1:]
            codewords = codewords[indexOf(codewords, '=')+1:]
        transcodedict = dict(zip(transwords,codewords))
        if not codewords:
            continue
#         label = re.sub('\d$', '', codewords[0])
#         codewords = ['array' if codeword in array else 'primitive' if codeword in primitive else 'mapping' for codeword in codewords]
#         print(codewords)
        important_words = [sentword in transwords and is_func(transcodedict[sentword]) and transcodedict[sentword] != 'return' for sentword in sentwords]
        labels = [ label if important_words[i] else labels[i] for i in range(N)]
        var_words = [sentword in transwords and sentword not in string.punctuation and not is_func(transcodedict[sentword]) for sentword in sentwords]
        labels = [ 'var' if var_words[i] else labels[i] for i in range(N)]
#     if labels == ['O'] * N:
#         return None
    return zip(sentwords, pos, features, labels)


def label_sentence(sentence,translations,code):
    '''
    
    :param sentence:
    :param translations:
    :param code:
    '''
    sentwords = nltk.word_tokenize(sentence.lower())
    pos = zip(*nltk.pos_tag(sentwords))[1]
    N = len(sentwords)
    labels = ['O'] * N
    for translation,codeline in zip(translations,code):
        codewords = nltk.word_tokenize(codeline)
        transwords = nltk.word_tokenize(translation)
        if not codewords:
            continue
#         codewords = ['array' if codeword in array else 'primitive' if codeword in primitive else 'mapping' for codeword in codewords]
#         print(codewords)
        labelwords = ['mapping' if is_func(codeword) else 'O' for codeword in codewords]
        relevantwords = list(set(sentwords) & set(transwords))
        relevantwords = [word for word in relevantwords if word not in string.punctuation]
        labels = [ labelwords[transwords.index(sentwords[i])] if sentwords[i] in relevantwords else labels[i] for i in range(N)]
    return zip(sentwords,pos,labels)

def label_problem(problem, only_code=True):
    '''
    label each sentence in the problem
    
    :param problem:
    :param only_code: should sentences without code be labeled
    '''
    parse = parse_problem(problem)
    problem_labels = []
    for sentence_parse in parse['sentences']:
        sentence = sentence_parse['sentence']
        translations = sentence_parse['translations']
        code = sentence_parse['code']
        if only_code and not code: #TODO: ?
            continue
#             labels = label_sentence(sentence, translations, code)
        labels = label_sentence_by_type(sentence, translations, code)
#         if not labels:
#             continue
        problem_labels.append(labels)
    return problem_labels 

def build_train(indir, outdir, only_code=True):
    '''
    build train database by labeling each problem in indir
    
    :param indir: path to problems to label
    :param outdir: path to write labeled problems
    :param only_code: should sentences without code be labeled
    '''
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    os.mkdir(outdir)
    for fname in sorted(os.listdir(indir)):
        if not fname.endswith('.py'):
            continue
        print(fname)
        with open(os.path.join(indir,fname),'r') as fp:
            problem = fp.read()
        problem_labels = label_problem(problem, only_code=only_code) 
        fileBase, fileExtension = os.path.splitext(fname)
        with open(os.path.join(outdir,fileBase+'.label'),'w') as f:
            f.write('\n\n'.join(['\n'.join(['\t'.join(label) for label in labels]) for labels in problem_labels]))

def get_label_probs(sentence, label, n=None):
    '''
    get probability for the given label, for each of the words in the sentence
    
    :param sentence: sentence in json format
    :param label:
    :param n: number of possible words for each label 
    '''
    sentprobs = []
    for line in sentence:
        important = line['label'] == label
        probs = {v: k for k, v in ast.literal_eval(line['probs'])}
        if label in probs:
            prob = probs[label]
        else:
            prob = 0
        sentprobs.append((prob,important,line['word'],sentence.index(line)))
    sentprobs = sorted(sentprobs,reverse = True)
    return sentprobs[:n]

def get_probable_label_words(sentence, label, n=None):
    '''
    get the words for the given label sorted by their probability
    
    :param sentence: sentence in json format
    :param label:
    :param n: number of possible words for each label 
    '''
    return zip(*get_label_probs(sentence, label, n))[-2]

def get_label_words(sentence, label):
    '''
    get the actual words for the given label
    
    :param sentence: sentence in json format
    :param label:
    '''
    label_words = []
    for line in sentence:
        if line['label'] == label:
            label_words.append((line['word'],sentence.index(line)))
    return label_words
    
def check_type(sentence, word_type, n):
    '''
    check whether the actual words of a certain word type are contained in the probable words for that word type 
    
    :param sentence: sentence in json format
    :param label:
    :param n: number of possible words for each label 
    '''
    print(word_type)
    sentprobs = get_label_probs(sentence, word_type, n)
    expected_words = zip(*sentprobs)[-1]
    label_words = get_label_words(sentence, word_type)
    if label_words:
        label_words = zip(*label_words)[-1]
        result = set(label_words).issubset(set(expected_words))
    else:
        result = True
#     result = all([not important for (sentprob,important,word) in sentprobs[n:]])
    if not result:
        logger.logging.info(word_type)
        logger.logging.info(sentprobs)
    return result

def check_problem(json_dir,fname,n, labels=types):
    '''
    check each label for the given problem
    
    :param json_dir: path to the problems
    :param fname: problem name
    :param n: number of possible words for each label 
    :param labels:
    '''
    with open(os.path.join(json_dir,fname),'r') as inputjson:
        problem_json = json.load(inputjson)
#     for problem in problems_json:
    problem_result = []
    for sentence in problem_json:
#         check if n most probable mappings contain all mappings
        for word_type in labels:
            result = check_type(sentence, word_type, n)
            problem_result.append(result)
#         result = check_type(sentence, 'var', n)
#         problem_result.append(result)
    return problem_result

def calc_score(json_dir, n, problem_dir=None, labels=types):
    '''
    calculate how many problems pass the check in the given path
    
    :param json_dir: path to the problems
    :param fname: problem name
    :param problem_dir: given to allow checking whether a problem has a solution 
    :param labels:
    '''
    correct = []
#     no_sol = []
    total = 0
    fnames = sorted(os.listdir(json_dir))
    for fname in fnames:
        if problem_dir and not check_solution(os.path.join(problem_dir, re.sub('.label', '.py', fname))):
#             no_sol.append(fname)
            continue
        problem_result = check_problem(json_dir, fname, n, labels)
        if any(problem_result) and all(problem_result):
            correct.append(fname)
        else:
            logger.logging.info(fname)
        total += any(problem_result)
#     print(total)
    if total:
        print(float(len(correct))/total)
    return correct

def main():
    
    indir = os.path.join('res','text&code6')
#     train_dir = 'res/word_train'
    train_dir = os.path.join(indir, 'word_train')
    fname = 'PalindromesCount.py'
#     fname = 'TextStatistics.py'
#     with open(os.path.join(indir,fname),'r') as fp:
#         problem = fp.read()
#     label_problem(problem)
#     build_train(indir, train_dir)

    test_indir = os.path.join('res', 'problems_test')
    test_dir = os.path.join(test_indir,'word_test')
#     build_train(test_indir, test_dir, only_code=False)

    output_dir = os.path.join(indir, 'word_json')
#     CRF.test(train_dir, output_dir)
    test_output_dir = os.path.join(test_indir, 'word_json')
#     CRF.test(train_dir, test_output_dir, test_dir)

    check_dir = output_dir
    m = 2
    print(calc_score(check_dir, m, indir))
#     scores = {}
#     for m in range(1,20):
#         scores[m] = len(calc_score(check_dir, m, indir))
#     print(scores)
#     import matplotlib.pyplot as plt
#     plt.plot(scores.values())
#     plt.ylabel('some numbers')
#     plt.show()
    
    fname = 'AverageAverage.label'
#     fname = 'BlockTower.label'
#     fname = 'ChocolateBar.label'
#     fname = 'CompetitionStatistics.label'
#     fname = 'CucumberMarket.label'
#     fname = 'DifferentStrings.label'
#     fname = 'FarFromPrimes.label'
#     fname = 'Elections.label'
#     fname = 'LittleElephantAndBallsAgain.label'
#     print(check_problem(output_dir, fname, m))


if __name__ == '__main__':
    main()