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
import subprocess
import threading
import doctest
import logger
import string
# from code_parser import clean_codeline


N = 2
input_array = range(N)
input_array0 = range(N)
input_array1 = range(N)
input_array2 = range(N)
types = range(N)
input_int = 0
input_int0 = 0
input_int1 = 0
input_int2 = 0
possibilities = list(subsets(input_array))
possibility = range(N)
possibility0 = range(N)
possibility1 = range(N)
possibility2 = range(N)
mapping = lambda possibility: N
mapping0 = lambda possibility: N
mapping1 = lambda possibility: N
mapping2 = lambda possibility: N
valid = lambda possibility: True
valid0 = lambda possibility: True
valid1 = lambda possibility: True
valid2 = lambda possibility: True
element = N

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

def check_solution_path(path):
    fail = []
    total = 0
#     not_empty = []
    for fname in sorted(os.listdir(path)):
        if not fname.endswith('.py'):
            continue
        print(fname)
        fpath = os.path.join(path, fname)
        if not check_solution(fpath):
            fail.append(fname)
        total += 1
    if total:
        print(len(fail)/float(total))
    return fail
            

def is_func(codeword):
    try:
        isfunc = codeword in ['return','reduce', 'mapping','valid'] or hasattr(eval(codeword), '__call__')
    except:
        isfunc = False
    return isfunc

def is_comparison(codeword):
    return codeword in [ 'lt', 'le', 'eq', 'ne', 'ge', 'gt']

def get_types(codes):
    try:
        return [type(eval(str(code))).__name__ for code in codes]
    except  (SyntaxError, TypeError, NameError) as e: #TODO: fix NameError in code
        logger.logging.debug(e)
        return []

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


def clean_codeline(codeline):
    '''
    >>> codeline = "reduce = (lambda possibility: ((indexOf(types, input_array[possibility[0]][possibility[1]]) + possibility[0]) + possibility[1]))"
    >>> print(clean_codeline(codeline))
    ((indexOf(types, input_array[possibility[0]][possibility[1]]) + possibility[0]) + possibility[1])
    
    >>> translation = "reduce = lambda possibility: (len(possibility) * excess(possibility))"
    >>> print(clean_codeline(translation))
    (len(possibility) * excess(possibility))
    
    
    >>> codeline = "def reduce(possibility): return len(set(possibility))"
    >>> print(clean_codeline(codeline))
    len(set(possibility))
    
    >>> codeline = "possibilities = sorted(input_array, key=itemgetter(input_int))"
    >>> print(clean_codeline(codeline))
    sorted(input_array, key=itemgetter(input_int))

    >>> codeline = "reduce = lambda possibility: (dps[i] * sum(hp[i:]))"
    >>> print(clean_codeline(codeline))
    (dps[i] * sum(hp[i:]))
    
    :param codeline:
    '''
    codeline = re.sub('^[^\(\:]+(\(lambda)?[^\:]+\:(?P<codeline>.+)(?(1)\))\s*', '\g<codeline>', codeline)
    codeline = re.sub('^[^=]+\=', '', codeline)
    codeline = re.sub('^.*return\s', '', codeline)
    codeline = codeline.strip()
    return codeline

def add_codeline_prefix(possible_codeline, word_type):
    if word_type == 'possibilities':
        possible_codeline = word_type + ' = ' + possible_codeline
    else:
        possible_codeline = word_type +' = lambda possibility: ' + possible_codeline
    return possible_codeline

def get_transdict(translation, codeline):
    codewords = nltk.word_tokenize(codeline)
    transwords = nltk.word_tokenize(translation)
    transdict = dict(zip(transwords,codewords))
    for k,v in transdict.items():
        if k in string.punctuation:
            del transdict[k]
    return transdict

codeline_types = ['mapping', 'valid', 'reduce', 'possibilities', 'return']
# types = ['mapping', 'valid', 'reduce']
# types = ['I']
def get_codeline_type(codeline):
    '''
    get word type from codewords
    
    :param codewords:
    '''
    codewords = nltk.word_tokenize(codeline)
    if not codewords:
        return ''
    word_type = clean_word(codewords[0])
    if word_type in codeline_types:
        return word_type
    if word_type == 'def' and clean_word(codewords[1]) in codeline_types:
        return clean_word(codewords[1])
    print(word_type)
    return ''


sentence_types = ['return', 'mapping', 'valid', 'reduce', 'possibilities']
# types = ['return', 'mapping', 'valid', 'reduce', 'possibilities', 'types']
# types = ['I']

def get_sentence_type(sentence, translations, code, method):
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
        if sentence_type in sentence_types:
            return sentence_type
    if len(code) == 1:
        codewords = nltk.word_tokenize(code[0])
        sentence_type = clean_word(codewords[0])
        if sentence_type in sentence_types:
            return sentence_type
        if sentence_type == 'def' and clean_word(codewords[1]) in sentence_types:
            return clean_word(codewords[1])
    else:
        codewords = nltk.word_tokenize(code[-1])
        if not method[0] and codewords[0] == 'return':
            return 'return'
#     print(method)
#     print(code)
    return 'O'

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
#     check_solution(problem_path)
    doctest.testmod()
    
    