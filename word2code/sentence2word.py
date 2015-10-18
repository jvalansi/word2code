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
    check_solution_path, get_codeline_type, codeline_types, clean_codeline,\
    get_transdict
from stanford_corenlp import tokenize_sentences
from CRF import Crf
from dependency_parser import get_features
import argparse



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
            label = get_codeline_type(codeline)
            if not label:
                continue
            translation = clean_codeline(translation)
            codeline = clean_codeline(codeline)
            transcodedict = get_transdict(translation, codeline)
            transwords = transcodedict.keys() 
            if not transcodedict:
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
        if not result:
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
            labels = codeline_types
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

    parser = argparse.ArgumentParser()
    parser.add_argument("-pd","--problem_dir", help="Directory of the problems to be labeled",
                        default=indir)
    parser.add_argument("-td", "--train_dir", help="Directory of the labeled problems")
    parser.add_argument("-od", "--outdir", help="Directory to store output")
    parser.add_argument("-m", "--M", help="Top M words allowed per label", type=int, default=1)
    parser.add_argument("-a", "--all", help="Whether to label all the sentences or only the ones with code", action="store_true")
    args = parser.parse_args()


    only_code = not args.all
    if not args.train_dir:
        args.train_dir = os.path.join(args.problem_dir, 'word_train')
    s2w.build_train(args.problem_dir, args.train_dir, only_code=only_code)

    if not args.outdir:
        args.outdir = os.path.join(args.problem_dir, 'word_json')
    s2w.test(args.train_dir, args.outdir)

    check_dir = args.outdir
    print(s2w.calc_score(check_dir, args.M, args.problem_dir))
    
    fname = 'MountainRanges.label'
#     fname = 'BlockTower.label'
#     fname = 'ChocolateBar.label'
    fname = 'CompetitionStatistics.json'
#     fname = 'CucumberMarket.label'
#     fname = 'DifferentStrings.label'
#     fname = 'FarFromPrimes.label'
#     fname = 'Elections.label'
#     fname = 'LittleElephantAndBallsAgain.label'
#     s2w.label_problem(indir, fname, train_dir)
#     print(s2w.check_problem(check_dir, fname, m))

if __name__ == '__main__':
    main()