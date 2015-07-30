'''
Created on Apr 2, 2015

@author: jordan
'''

import logger

import re
import os
from problem_parser import parse_problem
import shutil

from utils import check_solution, clean_name


class LearnerWrapper:
    
    
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
            self.label_problem(indir, fname, outdir, only_code=only_code) 
    
    
    
    def calc_score(self, json_dir, n, problem_dir=None, labels=None):
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
            if problem_dir and not check_solution(os.path.join(problem_dir, clean_name(fname)+'.py')):
                continue
            print(fname)
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


if __name__ == '__main__':
    pass
