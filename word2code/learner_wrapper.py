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
class LearnerWrapper():
    
    
    
    def label_problem(self, problem, only_code=True):
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
            labels = self.label_sentence_by_type(sentence, translations, code)
    #         if not labels:
    #             continue
            problem_labels.append(labels)
        return problem_labels 
    
    def build_train(self, indir, outdir, only_code=True):
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
            problem_labels = self.label_problem(problem, only_code=only_code) 
            fileBase, fileExtension = os.path.splitext(fname)
            with open(os.path.join(outdir,fileBase+'.label'),'w') as f:
                f.write('\n\n'.join(['\n'.join(['\t'.join(label) for label in labels]) for labels in problem_labels]))
    
    
    
    def calc_score(self, json_dir, n, problem_dir=None, labels=types):
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
            problem_result = self.check_problem(json_dir, fname, n, labels)
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
#     print(calc_score(check_dir, m, indir))
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