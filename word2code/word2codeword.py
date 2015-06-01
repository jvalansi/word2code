'''
Created on Apr 28, 2015

@author: jordan
'''
from __future__ import division
import logger
from nltk.corpus import wordnet as wn
import re
import csv
from itertools import product
import os
from problem_parser import parse_problem
import nltk
from collections import Counter
from utils import *
import w2v

wn_similarity = wn.wup_similarity

def wordnet_similarity(word1, word2):
    synsets1 = wn.synsets(word1)
    synsets2 = wn.synsets(word2)
    if not synsets1 or not synsets2:
        return -1
    try:
        sim_result = max(wn_similarity(synset1, synset2) for synset1,synset2 in product(synsets1,synsets2))
    except Exception:
        sim_result = -1 
    return sim_result
#     return max(wn.wup_similarity(synset1, synset2) for synset1,synset2 in product(synsets1,synsets2))
#     return max(wn.jcn_similarity(synset1, synset2) for synset1,synset2 in product(synsets1,synsets2))
#     return max(wn.lch_similarity(synset1, synset2) for synset1,synset2 in product(synsets1,synsets2))
#     return max(wn.lin_similarity(synset1, synset2) for synset1,synset2 in product(synsets1,synsets2))
#     return max(wn.path_similarity(synset1, synset2) for synset1,synset2 in product(synsets1,synsets2))
#     return max(wn.res_similarity(synset1, synset2) for synset1,synset2 in product(synsets1,synsets2))

def clean_word(word):
    word = re.sub('\d?$', '', word)
    word = word.strip()
    return word

def is_func(codeword):
    try:
        isfunc = codeword in ['return','reduce', 'mapping','valid'] or hasattr(eval(codeword), '__call__')
    except:
        isfunc = False
    return isfunc

def word2codewords(word, translations_count=None, p_thresh = 0.3, n=0):
    word = clean_word(word)
    if not word:
        return []
    likelihoods = []
    funcword_dict = {codeword: transword for codeword,transword in codeword_dict.items() if is_func(codeword)}
    translations_likelihoods = [(-1, codeword) for codeword, transword in funcword_dict.items()]
    w2v_likelihoods = [(-1, codeword) for codeword, transword in funcword_dict.items()]
    if translations_count:
        count_sum = sum(translations_count[(word, codeword)] in translations_count if (word, codeword) else 0 for codeword, transword in funcword_dict.items() )
        if count_sum > 1:
            translations_likelihoods = [(translations_count[(word, codeword)]/count_sum, codeword) if (word, codeword) in translations_count else (-1,codeword) for codeword, transword in funcword_dict.items() ]
#             likelihoods = sorted(likelihoods, reverse = True)
#             return likelihoods
    wordnet_likelihoods = [(wordnet_similarity(word.lower(), codeword_dict[codeword]), codeword) for codeword, transword in funcword_dict.items()]
#     likelihoods = sorted(likelihoods, reverse = True)
#     if likelihoods[0][0] >= p_thresh:
# #         print('wordnet')
#         return likelihoods
    try:
        w2v_likelihoods = [(w2v.model.similarity(word.lower(), codeword_dict[codeword]), codeword) for codeword, transword in funcword_dict.items()]
#         likelihoods = sorted(likelihoods, reverse = True)
#         if likelihoods[0][0] >= p_thresh:
# #             print('w2v')
#             return likelihoods
    except Exception:
        pass
    likelihoods = [(max(zip(*likelihood)[0]),zip(*likelihood)[1][0]) for likelihood in zip(w2v_likelihoods,translations_likelihoods, wordnet_likelihoods)]
    return likelihoods
#     if n:
#         return likelihoods[:n]
#     return likelihoods

def get_codeword_dict():
    codeword_dict = {}
    with open('res/codewords', 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            codeword_dict[row[0]] = clean_word(row[1])
    return codeword_dict

codeword_dict = get_codeword_dict()

def count_translations(path, fnames):
    translations_count = []
    for fname in fnames:
        with open(os.path.join(path,fname),'r') as f:
            problem = f.read()
        parse = parse_problem(problem)
        for sentence_parse in parse['sentences']:
            translations = sentence_parse['translations']
            code = sentence_parse['code']
            for translation,codeline in zip(translations,code):
                codewords = nltk.word_tokenize(codeline)
                transwords = nltk.word_tokenize(translation)
                if not codewords:
                    continue
                translations_count.extend(zip(transwords,codewords))
    return Counter(translations_count)

def get_translation_dict(translations, code):
    transdict = {}
    for translation,codeline in zip(translations,code):
        codewords = nltk.word_tokenize(codeline)
        transwords = nltk.word_tokenize(translation)
        transdict.update(dict(zip(transwords,codewords)))
    return transdict


def check_problem(path, fname, p_thresh):
    fnames = sorted(os.listdir(path))
#         count translations of all words in all other problems
    translations_count = count_translations(path, filter(lambda f: f != fname, fnames))
#     print(translations_count)
#         predict most likely (highest count) translation for words in the Problem
    results = []
    with open(os.path.join(path,fname),'r') as f:
        problem = f.read()
    parse = parse_problem(problem)
    for sentence_parse in parse['sentences']:
        sentence = sentence_parse['sentence']
        sentwords = nltk.word_tokenize(sentence)
        translations = sentence_parse['translations']
        code = sentence_parse['code']
        transdict = get_translation_dict(translations, code)
        for transword,codeword in transdict.items():
            if transword not in sentwords:
                continue
            if not is_func(codeword) or codeword  in ['reduce', 'mapping', 'valid']:
                continue
            likely_codewords = word2codewords(transword, translations_count, p_thresh)
            result = bool(likely_codewords) and codeword in [likely_codeword for p,likely_codeword in likely_codewords if p >= p_thresh]
            if not result:
                logger.logging.info(fname)
                logger.logging.info(transword)
                logger.logging.info(codeword)
                logger.logging.info(likely_codewords)
            results.append(result)
    return(all(results))

def check_words(path, p_thresh):
    successful = []
#     for each Problem
    fnames = sorted(os.listdir(path))
    for fname in fnames:
        if check_problem(path, fname, p_thresh):
            successful.append(fname)
    print(float(len(successful))/len(fnames))
    return successful


if __name__ == '__main__':
    p_thresh = 0
    problem_dir = 'res/text&code5'
    fname = 'CompetitionStatistics.py'
#     fname = 'ChocolateBar.py'
#     fname = 'Elections.py'
#     fname = 'Multiples.py'
    print(check_words(problem_dir, p_thresh))
#     print(check_problem(problem_dir, fname, p_thresh))

    results = []
    similarities = [wn.wup_similarity,
                wn.jcn_similarity,
                wn.lch_similarity,
                wn.lin_similarity,
                wn.path_similarity,
                wn.res_similarity]
    for sim in similarities:
        wn_similarity = sim
        sim_results = []
        for p in range(10):
            sim_results.append(len(check_words(problem_dir, p*0.1)))
        results.append(sim_results)
    print(results)

#     print(word2codewords('adjacent'))