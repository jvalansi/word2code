'''
Created on Apr 6, 2015

@author: jordan
'''
import re
import os
import json

def parse_problem(problem):
# from utils import *
# from operator import *
# 
# class AlienAndPassword:
#     # Alien Fred wants to destroy the Earth, but he forgot the password that activates the planet destroyer.
#     
#     # You are given a String S.
#     def getNumber(self, S):
#         input_array = numpy.array(list(S))
#         N = input_array.shape
#         possibilities = subsets(input_array)
# 
#     # Fred remembers that the correct password can be obtained from S by erasing exactly one character.
# 
#     # the correct array can be done from S by removing exactly 1 element
#     ####    correct = lambda array: exactly(len(removing(S, array)), 1)
#         valid = lambda possibility: eq(len(diff(input_array, possibility)), 1)
# 
#     # Return the number of different passwords Fred needs to try.
#     ####    return(number(different(possibility for possibility in passwords if valid(possibility))))
#         return(len(set(possibility for possibility in possibilities if valid(possibility))))
# 
# 
# if __name__ == '__main__':
#     S = 'aa'
#     aap = AlienAndPassword()
#     print(aap.getNumber(S))
    parse = {}

    import_pattern = '\s*import\s+\S+|from\s+.+\s+import\s+.+'
    parse['import'] = re.findall(import_pattern,problem) 
    class_pattern = '\s*class\s+.+:'
    parse['class'] = re.findall(class_pattern,problem) 
    method_pattern = '\s*def\s+.+\(self(?:\s*,\s*.+)*\)'
    parse['method'] = re.findall(method_pattern,problem) 
    main_pattern = '\s*if\s+__name__\s*==\s*\'__main__\'\s*:\s*\n(?:.+\n)+'
    parse['main'] = re.findall(main_pattern,problem) 
    sentences_pattern = '(?:\s*#[^#].+\n)(?:\s*####.+\n.+\n)*'
#     sentences_pattern = '(?:[ \t\r\f\v]*#[^#].+\n)+'
    sentences = re.findall(sentences_pattern,problem)
    parse['sentences'] = [parse_sentence(sentence) for sentence in sentences] 
    return parse

def parse_sentence(sentence):
    parse = {}
    comment_pattern = '(\s*#[^#].+\n)(?:\s*####.+\n.+\n)*'
    comments = re.findall(comment_pattern, sentence)
    parse['sentence'] = ' '.join([re.sub('^\s*#','',comment) for comment in comments])
    translation_pattern = '(?:\s*####(.+\n).+\n)'
    parse['translations'] = re.findall(translation_pattern, sentence)
    code_pattern = '(?:\s*####.+\n(.+\n))'
    parse['code'] = re.findall(code_pattern, sentence)
    return parse
    

def parse_dir(dir):
    parses = []
    for fname in os.listdir(dir):
        with open(fname,'r') as f:
            problem = f.read()
            parses.append(parse_problem(problem))
    return parses


if __name__ == '__main__':
    with open('res/text&code3/AmoebaDivTwo.py') as f:
        problem = f.read()
    parse = parse_problem(problem)
    with open('res/parse', 'w') as f:
        json.dump(parse,f,indent=4, separators=(',', ': '))