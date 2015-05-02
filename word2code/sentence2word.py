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

from utils import *
from collections import Counter
import codeline_gen
from word2codeword import word2codewords, clean_word, codeword_dict, is_func


mapping = lambda x: x
valid = lambda x: True
array = ['input_array','possibilities','types','possibility',]
primitive = ['j', 'i', 'inf', 'N','element','number','input_int', '0', '1', '2']
non_callable = set()
non_relevant = []


#     phrase to code:
#     phrase:         Return the number of different passwords Fred needs to try.
#     dependencies:    det(number-3, the-2)
#                      prep_return(needs-8, number-3)
#                      amod(passwords-6, different-5)
#                      prep_of(number-3, passwords-6)
#                      nsubj(needs-8, Fred-7)
#                      nsubj(try-10, Fred-7)
#                      root(ROOT-0, needs-8)
#                      aux(try-10, to-9)
#                      xcomp(needs-8, try-10)
#                     return(number(different(passwords(needs(Fred,try)))
#                     return(number(different(possibility for possibility in passwords if valid(possibility))))
#     code:           return(len(set(possibility for possibility in possibilities if valid(possibility))))
#     
#     phrase:         the correct array can be done from S by removing exactly 1 element
#                     det(array-3, the-1)
#                     amod(array-3, correct-2) correct = lambda array: 
#                     nsubjpass(done-6, array-3) 
#                     aux(done-6, can-4)
#                     auxpass(done-6, be-5)
#                     root(ROOT-0, done-6)
#                     prep_from(done-6, S-8)
#                     agent(done-6, removing-10)
#                     advmod(element-13, exactly-11)
#                     num(element-13, 1-12)
#                     dobj(removing-10, element-13) - removing
#     ROOT(done(array(correct),S,removing(element(exactly,1)))
#     ####    correct = lambda array: exactly(len(removing(S, array)), 1)
#     code:   valid = lambda possibility: eq(len(diff(input_array, possibility)), 1)
#     
#     every cell of the table covered by the amoeba must only contain antimatter.
#                     det(cell-2, every-1)
#                     nsubj(contain-12, cell-2)
#                     det(table-5, the-4)
#                     prep_of(cell-2, table-5)
#                     vmod(table-5, covered-6)
#                     det(amoeba-9, the-8)
#                     agent(covered-6, amoeba-9)
#                     aux(contain-12, must-10)
#                     advmod(contain-12, only-11)
#                     root(ROOT-0, contain-12)
#                     dobj(contain-12, antimatter-13)
#     ROOT(contain(cell(every,table(covered(amoeba)),must,only,antimatter)))
#     ####    valid = lambda amoeba:     every(contain(cell, antimatter[0]) for cell of table if covered(cell, amoeba))
#             valid = lambda possibility: all(contains(element, types[0]) for element in input_array if contains(element, possibility))




        

def label_sentence(sentence,translations,code):
    sentwords = nltk.word_tokenize(sentence.lower())
    pos = zip(*nltk.pos_tag(sentwords))[1]
    N = len(sentwords)
    labels = ['O'] * N  
    for translation,codeline in zip(translations,code):
        codewords = nltk.word_tokenize(codeline)
        transwords = nltk.word_tokenize(translation)
        if not codewords:
            continue
#         codewords = ['array' if codeword in array else 'primitive' if codeword in primitive else 'mapping' for codeword in codewords]
#         print(codewords)
        labelwords = ['mapping' if is_func(codeword) else 'O' for codeword in codewords]
        relevantwords = list(set(sentwords) & set(transwords))
        relevantwords = [word for word in relevantwords if word not in string.punctuation]
        labels = [ labelwords[transwords.index(sentwords[i])] if sentwords[i] in relevantwords else labels[i] for i in range(N)]
    return zip(sentwords,pos,labels)

def build_train(indir, outdir):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    for fname in os.listdir(indir):
        with open(os.path.join(indir,fname),'r') as f:
            problem = f.read()
        parse = parse_problem(problem)
        problem_labels = []
        for sentence_parse in parse['sentences']: 
            sentence = sentence_parse['sentence']
            translations = sentence_parse['translations']
            code = sentence_parse['code']
            if not sentence or not code:
                continue
            labels = label_sentence(sentence, translations, code)
            problem_labels.append(labels)
        fileBase, fileExtension = os.path.splitext(fname)
        with open(os.path.join(outdir,fileBase+'.label'),'w') as f:
            f.write('\n\n'.join(['\n'.join(['\t'.join(label) for label in labels]) for labels in problem_labels]))
         
                
def get_label_probs(sentence, label):
    sentprobs = []
    for line in sentence:
        important = line['label'] == label
        probs = {v: k for k, v in ast.literal_eval(line['probs'])}
        prob = probs[label]
        sentprobs.append((prob,important,line['word']))
    sentprobs = sorted(sentprobs,reverse = True)
    return sentprobs
                  
def calc_score(json_dir,n):
    correct = []
    total = 0
    fnames = sorted(os.listdir(json_dir))
    for fname in fnames:
        with open(os.path.join(json_dir,fname),'r') as inputjson:
            problem_json = json.load(inputjson)
#     with open(json_name,'r') as inputjson:
#         problems_json = json.load(inputjson)
#     for problem in problems_json:
#         check if n most probable mappings contain all mappings
        problem_result = []
        for sentence in problem_json:
            sentprobs = get_label_probs(sentence, 'mapping')
            result = all([not important for (sentprob,important,word) in sentprobs[n:]])
            if not result:
                print(sentprobs)
            problem_result.append(result)
        if all(problem_result):
            correct.append(fname)
        total += 1
    print(total)
    print(float(len(correct))/total)
    return correct
                  
                  
if __name__ == '__main__':
#     phrase = 'the correct array can be done from S by remove exactly 1 element'
#     phrase = 'Return the number of different passwords Fred needs to try.'
#     phrase2codewords(phrase)

#     word = 'top'
#     codeword = 'successive'
#     print(w2v.model.similarity(word.lower(), codeword))
#     print(word2codewords(word))
    
    indir = 'res/text&code3/'
#     print(check_sentences(indir,4))
#     print(Counter(non_relevant))

    outdir = 'res/code_train'
    build_train(indir, outdir)
    print(non_callable)
  
    dir = outdir
    output_dir = 'res/code_test'
    CRF.test(dir, output_dir)
     
    json_dir = 'res/code_json'
    CRF.output2json(output_dir, json_dir)
     
    print(calc_score(json_dir, 6))

#     funcs = ['indexOf', 'sorted', 'itemgetter']
#     vars = ['input_array', 'input_int']
#     possible_code = get_possible_code(funcs, vars)
#     print(len(possible_code))
#     with open('res/possible_code','w') as f:
#         f.write('\n'.join(possible_code))