'''
Created on Apr 6, 2015

@author: jordan
'''
#     extract significant phrases from problem
import nltk
import os
import string
import json
import ast
import logger
from itertools import combinations, combinations_with_replacement
from utils import check_solution, clean_word, clean_name
from stanford_corenlp import tokenize_sentences
from CRF import Crf
from dependency_parser import get_features


types = ['return', 'mapping', 'valid', 'reduce', 'possibilities']
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
        codewords = nltk.word_tokenize(method[0])
        sentence_type = clean_word(codewords[1])
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

def get_min_mask(sentwords,relevantwords):
    '''
    get minimal continuous subset containing all relevant words
    example:
            sentence words: ["hello", "world", ",", "how", "are", "you", "?"]
            relevant words: ["world", "are"]
            smallest csubset: ["world", ",", "how", "are"]
    
    :param sentwords:
    :param relevantwords:
    '''
    N = len(sentwords)
    mask = [1] * N
    for i,j in combinations_with_replacement(range(N), 2):
        if relevantwords.issubset(sentwords[i:j]):
            new_mask = [0] * N
            new_mask[i:j] = [1] * (j-i)
            if sum(new_mask) < sum(mask):
                mask = new_mask
    return mask

class Problem2Sentence(Crf):
    
    
    def label_sentence(self, sentence, translations, code, method):
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
#         symbol = symbol if symbol == 'O' else 'I'
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
            
    def get_probable_sentence_label(self, sentences_json, sentence, n, labels=types):
        '''
        get the most probable sentence type for the given sentence
        
        :param sentences_json:
        :param sentence:
        :param n: number of possible sentences for each type
        :param labels:
        '''
        possible_types = []
        sentind = sentences_json.index(sentence)
        for sentence_type in labels:
            sentprobs = self.get_sentences_probabilities(sentences_json, sentence_type, n)
            for sentprob in sentprobs:
                if sentind == sentprob[-1]:
                    possible_types.append((sentprob[0], sentence_type))
        if not possible_types:
            return None
        possible_types = sorted(possible_types, reverse=True)[0]
        return possible_types[-1]
    
    def get_sentences_probabilities(self, problem_json, label, n=None):
        '''
        get probability for the given label, for each of the sentence in the problem    
        
        :param problem_json:
        :param label:
        :param n: number of possible sentences for each type
        '''
        problem_probs = []
        for i,sentence in enumerate(problem_json):
            sentprobs = []
            for line in sentence:
                line_probs = {v: k for k, v in ast.literal_eval(line['probs'])}
                label_prob = line_probs[label] if label in line_probs else 0
                sentprobs.append(label_prob)
            sentprob = max(sentprobs)
            problem_probs.append((sentprob,i))
        problem_probs = sorted(problem_probs,reverse = True)
        return problem_probs[:n]
    
    def get_expected_sents(self, problem_json, symbol): 
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
    
    def get_expected_sentence_label(self, sentence, labels=types):
        '''
        get the actual type for the given sentence
        
        :param sentence:
        '''
        for line in sentence:
            if line['label'] in labels:
                return line['label']
            
    def check_problem(self, json_dir,fname,n, labels=None):
        '''
        check whether the probable label match the expected label
        
        :param json_dir:
        :param fname:
        :param n:
        :param labels:
        '''
    #         check if n most probable sentences contain all important sentences
        if not labels:
#             labels = ['I']
            labels = types
        with open(os.path.join(json_dir,fname),'r') as inputjson:
            problem_json = json.load(inputjson)
        results = []
        for sentence in problem_json:
            expected_type = self.get_expected_sentence_label(sentence, labels)
            expected_type_sentprobs = self.get_sentences_probabilities(problem_json,expected_type)
            probable_type = self.get_probable_sentence_label(problem_json, sentence, n, labels)
            probable_type_sentprobs = self.get_sentences_probabilities(problem_json,probable_type)
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


def main():
    p2s = Problem2Sentence()
    indir = os.path.join('res', 'text&code7')
    train_dir = os.path.join(indir, 'sentence_train')
#     p2s.build_train(indir, train_dir)

    test_indir = os.path.join('res', 'problems_test1')
    test_dir = os.path.join(test_indir, 'sentence_test')
#     p2s.build_train(test_indir, test_dir, only_code=False)

    outdir = os.path.join(indir, 'sentence_json')
#     p2s.test(train_dir, outdir)

    test_outdir = os.path.join(test_indir, 'sentence_json')
#     p2s.test(train_dir, test_outdir, test_dir)

    n = 3
    n = 1
#     print(p2s.calc_score(outdir, n, indir))

    fname = 'AverageAverage.label'
    fname = 'ChocolateBar.label'
    fname = 'CompetitionStatistics.label'
#     fname = 'ChristmasTreeDecorationDiv2.label'
#     fname = 'Elections.label'
#     fname = 'FarFromPrimes.label'
#     fname = 'LittleElephantAndBallsAgain.label'
    fname = 'ChocolateBar.py'
    fname = 'MeasuringTemperature.py'
    fname = 'SwappingDigits.py'
#     fname = 'TheEquation.py'
    p2s.label_problem(indir, fname, train_dir)
    p2s.test_file(train_dir, clean_name(fname)+'.label', outdir)
#     print(check_problem(outdir, fname, n))



if __name__ == '__main__':
    main()
