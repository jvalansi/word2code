'''
Created on Jul 23, 2015

@author: jordan
'''

import imp
import os
import json
import nltk
import collections
import re
from problem_utils import *
import resource
import subprocess
import threading

K = 1024
M = K*K

def clean_name(fname):
    return os.path.splitext(fname)[0]

def clean_word(word):
    word = re.sub('\d?$', '', word)
    word = word.strip()
    return word

class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout=None):
        def target():
            print 'Thread started'
            self.process = subprocess.Popen(self.cmd, shell=True)
            self.process.communicate()
            print 'Thread finished'

        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout)
        if thread.is_alive():
            print 'Terminating process'
            self.process.terminate()
            thread.join()

def check_solution_(problem_path):#TODO: make it portable
    problem_path = os.path.abspath(problem_path)
    limit_cmd = 'ulimit -v '+str(1*M)
    cmd = limit_cmd+'; '+'python \"'+problem_path+'\"'
    try:
        result = subprocess.check_output(cmd, shell=True)
    
    #     command = Command(cmd)
    #     command.run()
    #     result = command.process.stdout
    
        return eval(result)
    except Exception:
        pass
    return False

def check_solution(problem_path, soln=1):
#     resource.setrlimit(resource.RLIMIT_DATA, (M, 100*M))   
    try:
        

        if os.path.exists(problem_path+'c'):
            os.remove(problem_path+'c')
        temp = imp.load_source('tmp', problem_path)
        for i in range(soln):
            name = 'example' + str(i)
            if hasattr(temp, name):
                result = getattr(temp, name)() 
            if not result:
                return False
        return True
    except Exception:
#         traceback.print_exc()
        pass
    return False


def is_func(codeword):
    try:
        isfunc = codeword in ['return','reduce', 'mapping','valid'] or hasattr(eval(codeword), '__call__')
    except:
        isfunc = False
    return isfunc

class WordCount:
    def get_data(self,data_dir,suffix):
        data = []
        for fn in os.listdir(data_dir):
            if not fn.endswith(suffix):
                continue
            f = open(os.path.join(data_dir,fn),'r')
            data.append(f.read())
        return data

    def tuple2file(self,t,data_name):
        with open('res/count_'+data_name+'.txt', 'w') as f:
            json.dump(t, f, ensure_ascii=False, indent = 4, separators=[',',': '])

    def count_words(self,data,data_name):
        tokens = nltk.word_tokenize(data)
        c = collections.Counter(tokens)
        c = sorted(c.items(), key=lambda item: item[1],reverse = True)
        self.tuple2file(c, data_name)
        return c

    def cnt2rank(self,cnt,name):
        words,word_cnts = zip(*cnt)
        rank = enumerate(words)
        d = dict((y,x) for x,y in rank)
        self.tuple2file(tuple(rank), 'rank_'+name)
        return d


    def compare_count(self,data_dir,word):
#         rank words in problem
        prb_data = self.get_data(data_dir,'prb')
        word_cnt = self.count_words('\n'.join(prb_data), 'prb')
        word_rank = self.cnt2rank(word_cnt,'word')
        word_cnt = dict((x,y) for x,y in word_cnt)
        print(word_rank)
#         rank words in problems where solution contains word
        sol_data = self.get_data(data_dir,'sol')
        fltr_data = [prb_data[i] for i in range(len(prb_data)) if word in sol_data[i]]
        fltr_cnt = self.count_words('\n'.join(fltr_data), 'fltr')
        fltr_rank = self.cnt2rank(fltr_cnt,'fltr')
        fltr_cnt = dict((x,y) for x,y in fltr_cnt)
#         print(fltr_rank)
#          get most significant change
        print([word for word in fltr_rank if word not in word_rank])
        diff = ((word,float(fltr_cnt[word]) / word_cnt[word]) for word in fltr_cnt if word in word_cnt)
        diff = sorted(diff, key=lambda item: item[1],reverse = True)
        print(diff)
        self.tuple2file(diff, 'diff')


if __name__ == '__main__':
#     main_data_dir = 'res/brute_force_easy/'
#     wc = WordCount()
#     wc.compare_count(main_data_dir, '>')

#     fpath = 'res/intersection'
#     with open(fpath) as f:
#         data = f.read()
#     wc.count_words(data, 'intersection')
    problem_path = 'res/text&code6/solutions_struct/TextStatistics.py' 
#     problem_path = 'res/text&code6/solutions_struct/AverageAverage.py' 
#     problem_path = 'res/text&code6/solutions_struct/ArrayHash.py' 
#     problem_path = 'test.py'
    check_solution(problem_path)
