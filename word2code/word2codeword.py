'''
Created on Apr 28, 2015

@author: jordan
'''
from __future__ import division
import logger
from nltk.corpus import wordnet as wn
import csv
from itertools import product
import os
from problem_parser import parse_problem
import nltk
from collections import Counter
import w2v
from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import SnowballStemmer 
from nltk.stem import WordNetLemmatizer
from utils import is_func, check_solution, clean_word

wn_similarity = wn.wup_similarity
# stemmer = SnowballStemmer('english')
# stemmer = PorterStemmer()
# stemmer = LancasterStemmer()
stemmer = WordNetLemmatizer()

model = None

def wordnet_similarity(word1, word2):
    '''
    calculate words similarity using wordnet 
    
    :param word1:
    :param word2:
    '''
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


def get_translations_likelihoods(word, translations_count, funcword_dict):
    '''
    get likelihoods of translations of the given word according to their count in the data
    
    :param word:
    :param translations_count:
    :param funcword_dict:
    '''
    translations_likelihoods = [(-1, codeword) for codeword, transword in funcword_dict.items()]
    if not translations_count:
        return translations_likelihoods
    stem = stemmer.lemmatize(word, 'v')
    translations_likelihoods = [(translations_count[(stem, codeword)], codeword) if (stem, codeword) in translations_count else (0, codeword) for codeword, transword in funcword_dict.items()]
    count_sum = sum(zip(*translations_likelihoods)[0])
    if not count_sum > 1:
        return translations_likelihoods
    translations_likelihoods = [(likelihood/count_sum, codeword)  for likelihood, codeword in translations_likelihoods]
    return translations_likelihoods

def get_wordnet_likelihoods(word, funcword_dict):
    '''
    get likelihoods of translations of the given word according to their wordnet similarity
    
    :param word:
    :param funcword_dict:
    '''
    stem = stemmer.lemmatize(word, 'v')
    wordnet_likelihoods = [(wordnet_similarity(stem, codeword_dict[codeword]), codeword) for codeword, transword in funcword_dict.items()]
    return wordnet_likelihoods

def get_w2v_likelihoods(word, model, funcword_dict):
    '''
    get likelihoods of translations of the given word according to their word2vec similarity
    
    :param word:
    :param model:
    :param funcword_dict:
    '''
    stem = stemmer.lemmatize(word, 'v')
    if not model or stem not in model.vocab:
        return [(-1, codeword) for codeword, transword in funcword_dict.items()]
    w2v_likelihoods = [(model.similarity(stem, codeword_dict[codeword]), codeword) if codeword_dict[codeword] in model.vocab else (-1, codeword) for codeword, transword in funcword_dict.items()]
    return w2v_likelihoods

def get_model():
    global model
    if not model:
        model = w2v.W2V().model
    return model

def word2codewords(word, translations_count=None, p_thresh=0.3, p=None):
    '''
    generate most p most probable codewords for the given word
    
    :param word:
    :param translations_count:
    :param p_thresh: minimal probability to trust a certain likelihood 
    :param p: number of possible codewords for each word
    '''
    word = clean_word(word)
    if not word:
        return []
    funcword_dict = {codeword: transword for codeword,transword in codeword_dict.items() if is_func(codeword)}
    translations_likelihoods = get_translations_likelihoods(word, translations_count, funcword_dict)
    if max(zip(*translations_likelihoods)[0]) >= p_thresh:
        likelihoods = sorted(translations_likelihoods, reverse=True)[:p]
        return likelihoods
    wordnet_likelihoods = get_wordnet_likelihoods(word, funcword_dict)
    if max(zip(*wordnet_likelihoods)[0]) >= p_thresh:
        likelihoods = sorted(wordnet_likelihoods, reverse=True)[:p]
        return likelihoods
    model = get_model()
    w2v_likelihoods = get_w2v_likelihoods(word, model, funcword_dict)
    if max(zip(*w2v_likelihoods)[0]) >= p_thresh:
        likelihoods = sorted(w2v_likelihoods, reverse=True)[:p]
        return likelihoods
    likelihoods = [(max(zip(*likelihood)[0]),zip(*likelihood)[1][0]) for likelihood in zip(w2v_likelihoods,translations_likelihoods, wordnet_likelihoods)]
#     likelihoods = [(max(zip(*likelihood)[0]),zip(*likelihood)[1][0]) for likelihood in zip(w2v_likelihoods,translations_likelihoods)]
    likelihoods = sorted(likelihoods, reverse=True)[:p]
    return likelihoods
#     if n:
#         return likelihoods[:n]
#     return likelihoods

def get_codeword_dict():
    '''
    get codeword dictionary from file
    '''
    with open(os.path.join('res', 'codewords'), 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        codeword_dict = {row[0]: clean_word(row[1]) for row in spamreader}
    return codeword_dict

codeword_dict = get_codeword_dict()

def count_translations(path, fnames):
    '''
    count the translations of every word of every problem in fnames
    
    :param path: path to the problems
    :param fnames: problem names to include
    '''
    translations_count = []
    for fname in fnames:
        if not fname.endswith('.py'):
            continue
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
                transwords = map(clean_word, transwords)
                stemwords = map(lambda word: stemmer.lemmatize(word, 'v'), transwords)
                translations_count.extend(zip(stemwords,codewords))
    return Counter(translations_count)

def get_translation_dict(translations, code, stem=True):
    '''
    dictionary of codewords and their respective translations  
    
    :param translations:
    :param code:
    :param stem:
    '''
    transdict = {}
    for translation,codeline in zip(translations,code):
        codewords = nltk.word_tokenize(codeline)
        transwords = nltk.word_tokenize(translation)
        if stem:
            transwords = [stemmer.lemmatize(word, 'v') for word in transwords]
        transdict.update(dict(zip(transwords,codewords)))
    return transdict


def check_problem(path, fname, p):
    '''
    check whether each of the codewords in the problem are contained in the probable codewords 
    
    :param path: path to problem
    :param fname: problem name
    :param p: number of possible codewords for each word
    '''
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
#             likely_codewords = word2codewords(transword, translations_count, p_thresh)
            likely_codewords = word2codewords(transword, translations_count, p=p)
#             result = bool(likely_codewords) and codeword in [likely_codeword for p,likely_codeword in likely_codewords if p >= p_thresh]
            likely_codewords = zip(*likely_codewords)[-1]
            result = codeword in likely_codewords 
            if not result:
                logger.logging.info(fname)
                logger.logging.info(clean_word(transword))
                logger.logging.info(stemmer.lemmatize(transword, 'v'))
                logger.logging.info(codeword_dict[codeword])
                logger.logging.info(codeword)
                try:
                    logger.logging.info(model.similarity(stemmer.lemmatize(transword, 'v'), codeword_dict[codeword]))
                except Exception:
                    pass
                logger.logging.info(likely_codewords)
            results.append(result)
    return(all(results))

def check_words(path, p):
    '''
    calculate how many problems pass the check in the given path
    
    :param path:
    :param p: number of possible codewords for each word
    '''
    successful = []
    total = 0
#     for each Problem
    fnames = sorted(os.listdir(path))
    for fname in fnames:
        if not fname.endswith('.py'):
            continue
        if not check_solution(os.path.join(path, fname)):
            continue
        if check_problem(path, fname, p):
            successful.append(fname)
        total += 1
#     print(total)
    print(float(len(successful))/total)
    return successful


def main():
    p_thresh = 1
    p = 1
    problem_dir = 'res/text&code6'
#     print(check_words(problem_dir, p_thresh))
#     print(check_words(problem_dir, p))
    fname = 'AverageAverage.py'
#     fname = 'AlienAndPassword.py'
#     fname = 'BasketsWithApples.py'
#     fname = 'CandidatesSelectionEasy.py'
#     fname = 'CompetitionStatistics.py'
#     fname = 'ChocolateBar.py'
#     fname = 'CucumberMarket.py'
#     fname = 'Elections.py'
#     fname = 'MarbleDecoration.py'
#     fname = 'MountainRanges.py'
#     fname = 'Multiples.py'
    p = 4
#     print(check_problem(problem_dir, fname, p))

    results = {}
    for p in range(1,20):
        results[p] = check_words(problem_dir, p)
    print(', '.join(['{}: {}'.format(k, len(v)) for k, v in results.items()]))
         
#     problem_dir = 'res/text&code5'
#     1: 19, 2: 20, 3: 22, 4: 23, 5: 23, 6: 23, 7: 23, 8: 23, 9: 24, 10: 24, 11: 24, 1
#     2: 24, 13: 24, 14: 24, 15: 25, 16: 26, 17: 26, 18: 29, 19: 30        
        
#     problem_dir = 'res/text&code6'
#     1: 38, 2: 39, 3: 40, 4: 41, 5: 41, 6: 41, 7: 41, 8: 41, 9: 42, 10: 42, 11: 42, 1
#     2: 42, 13: 42, 14: 42, 15: 43, 16: 44, 17: 44, 18: 46, 19: 46

#     results = []
#     similarities = [wn.wup_similarity,
#                 wn.jcn_similarity,
#                 wn.lch_similarity,
#                 wn.lin_similarity,
#                 wn.path_similarity,
#                 wn.res_similarity]
#     for sim in similarities:
#         wn_similarity = sim
#         sim_results = []
#         for p in range(10):
#             sim_results.append(len(check_words(problem_dir, p*0.1)))
#         results.append(sim_results)
#     print(results)

#     print(wordnet_similarity('most', 'maximum'))
#     print(word2codewords('adjacent'))

if __name__ == '__main__':
    main()