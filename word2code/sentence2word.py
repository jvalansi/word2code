'''
Created on Apr 2, 2015

@author: jordan
'''

import logger

import nltk
import os
import string
import json
import ast

from matplotlib.pyplot import imshow
from utils import is_func, check_solution, clean_name, clean_word,\
    check_solution_path
from stanford_corenlp import tokenize_sentences
from CRF import Crf
from dependency_parser import get_features


types = ['mapping', 'valid', 'reduce', 'possibilities', 'return']
# types = ['mapping', 'valid', 'reduce']
# types = ['I']
def get_type(codewords):
    '''
    get word type from codewords
    
    :param codewords:
    '''
    if not codewords:
        return ''
    word_type = clean_word(codewords[0])
    if word_type in types:
        return word_type
    if word_type == 'def' and clean_word(codewords[1]) in types:
        return clean_word(codewords[1])
    print(word_type)
    return ''

class Sentence2Word(Crf):

    
    
    def label_sentence(self, sentence, translations, code, method):
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
                transwords = transwords[transwords.index(':')+1:]
                codewords = codewords[codewords.index(':')+1:]
            if '=' in transwords:
                transwords = transwords[transwords.index('=')+1:]
                codewords = codewords[codewords.index('=')+1:]
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
        
    
    def get_label_probs(self, sentence, label, n=None):
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
    
    def get_probable_label_words(self, sentence, label, n=None):
        '''
        get the words for the given label sorted by their probability
        
        :param sentence: sentence in json format
        :param label:
        :param n: number of possible words for each label 
        '''
        return zip(*self.get_label_probs(sentence, label, n))[-2]
    
    def get_expected_label_words(self, sentence, label):
        '''
        get the actual words for the given label
        
        :param sentence: sentence in json format
        :param label:
        '''
        label_words = []
        for line in sentence:
            if line['label'] == label:
#                 label_words.append((line['word'],sentence.index(line)))
                label_words.append(line['word'])
        return label_words
        
    def check_type(self, sentence, word_type, n):
        '''
        check whether the actual words of a certain word type are contained in the probable words for that word type 
        
        :param sentence: sentence in json format
        :param label:
        :param n: number of possible words for each label 
        '''
        probable_words = self.get_probable_label_words(sentence, word_type, n)
        expected_words = self.get_expected_label_words(sentence, word_type)
        result = set(expected_words).issubset(set(probable_words))
    #     result = all([not important for (sentprob,important,word) in sentprobs[n:]])
#         if not result:
        logger.logging.info(word_type)
        logger.logging.info(set(probable_words))
        logger.logging.info(set(expected_words))
        return result
    
    def check_problem(self, json_dir,fname,n, labels=None):
        '''
        check each label for the given problem
        
        :param json_dir: path to the problems
        :param fname: problem name
        :param n: number of possible words for each label 
        :param labels:
        '''
        if not labels:
            labels = types
        with open(os.path.join(json_dir,fname),'r') as inputjson:
            problem_json = json.load(inputjson)
    #     for problem in problems_json:
        problem_result = []
        for sentence in problem_json:
    #         check if n most probable mappings contain all mappings
            for word_type in labels:
                result = self.check_type(sentence, word_type, n)
                problem_result.append(result)
    #         result = check_type(sentence, 'var', n)
    #         problem_result.append(result)
        return problem_result

def main():
    s2w = Sentence2Word()
    
    indir = os.path.join('res','text&code8')

    fname = 'PalindromesCount.py'
    fname = 'RandomColoringDiv2.py'
    train_dir = os.path.join(indir, 'word_train')
#     s2w.label_problem(indir, fname, train_dir)
#     s2w.build_train(indir, train_dir, only_code=True)

    test_indir = os.path.join('res', 'problems_test1')
    test_indir = indir
    test_dir = os.path.join(test_indir,'word_test')
#     s2w.build_train(test_indir, test_dir)

    output_dir = os.path.join(indir, 'word_json')
#     s2w.test(train_dir, output_dir)

    test_output_dir = os.path.join(test_indir, 'word_test_json')
#     s2w.test(train_dir, test_output_dir, test_dir)

    check_dir = output_dir
    m = 2
    print(s2w.calc_score(check_dir, m, indir))
#     scores = {}
#     for m in range(1,20):
#         scores[m] = len(calc_score(check_dir, m, indir))
#     print(scores)
#     import matplotlib.pyplot as plt
#     plt.plot(scores.values())
#     plt.ylabel('some numbers')
#     plt.show()
    
    fname = 'MountainRanges.label'
#     fname = 'BlockTower.label'
#     fname = 'ChocolateBar.label'
    fname = 'CompetitionStatistics.json'
#     fname = 'CucumberMarket.label'
#     fname = 'DifferentStrings.label'
#     fname = 'FarFromPrimes.label'
#     fname = 'Elections.label'
#     fname = 'LittleElephantAndBallsAgain.label'
#     print(s2w.check_problem(check_dir, fname, m))

if __name__ == '__main__':
    main()