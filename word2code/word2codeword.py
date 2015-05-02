'''
Created on Apr 28, 2015

@author: jordan
'''
import logger
from nltk.corpus import wordnet as wn
import re
import csv
from itertools import product
import os
from problem_parser import parse_problem
import nltk
from collections import Counter
import w2v



def wordnet_similarity(word1, word2):
    synsets1 = wn.synsets(word1) 
    synsets2 = wn.synsets(word2)
    if not synsets1 or not synsets2:
        return -1
    return max(wn.path_similarity(synset1, synset2) for synset1,synset2 in product(synsets1,synsets2))

def clean_word(word):
    return re.sub('[^a-zA-Z]', '',word)

def is_func(codeword):         
    try:
        isfunc = codeword in ['return','mapping','valid'] or hasattr(eval(codeword), '__call__')
    except:
        isfunc = False
    return isfunc

def word2codewords(word,n=0, translations_count=None):
    word = clean_word(word)
    if not word:
        return []
    likelihoods = []
    if translations_count:
        funcword_dict = {codeword: transword for codeword,transword in codeword_dict.items() if is_func(codeword)}    
        count_sum = sum(translations_count[(word, codeword)] for codeword,transword in funcword_dict.items() if (word, codeword) in translations_count)
        if count_sum > 1:
            likelihoods = [(float(translations_count[(word, codeword)])/count_sum, codeword) for codeword,transword in funcword_dict.items() if (word, codeword) in translations_count]
            return sorted(likelihoods, reverse = True)
    likelihoods = [(wordnet_similarity(word.lower(), codeword_dict[codeword]),codeword) for codeword,transword in funcword_dict.items()]
    likelihoods = sorted(likelihoods, reverse = True)
    if likelihoods[0][0] >= 0.3:
        return likelihoods
    try:
        likelihoods = [(w2v.model.similarity(word.lower(), codeword_dict[codeword]),codeword) for codeword,transword in funcword_dict.items()]
        likelihoods = sorted(likelihoods, reverse = True)
        if likelihoods[0][0] >= 0.3:
            return likelihoods
    except:
        pass
    return None
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

def check_words(path):
    successful = []
#     for each Problem
    fnames = sorted(os.listdir(path))
    for fname in fnames:
#         count translations of all words in all other problems
        translations_count = count_translations(path, filter(lambda f: f != fname, fnames))
#         print(translations_count)
#         predict most likely (highest count) translation for words in the Problem
        results = []
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
                for transword,codeword in zip(transwords,codewords):
                    if not is_func(codeword) or codeword == 'mapping' or codeword == 'valid':
                        continue 
                    logger.logging.info(codeword)
                    likely_codewords = word2codewords(transword, 0, translations_count)
                    logger.logging.info(likely_codewords)
                    result = bool(likely_codewords) and codeword in [likely_codeword for p,likely_codeword in likely_codewords if p >= 0.3]
                    logger.logging.info(result)
                    results.append(result)
        if all(results):
            successful.append(fname)
    print(float(len(successful))/len(fnames))
    return successful



            
if __name__ == '__main__':

    print(check_words('res/text&code3'))