'''
Created on Jun 14, 2015

@author: jordan
'''
from stanford_corenlp import tokenize_sentences
# import sentence2word
import nltk
import os
from problem_parser import parse_problem
from pystruct.models.edge_feature_graph_crf import EdgeFeatureGraphCRF
from pystruct.learners.one_slack_ssvm import OneSlackSSVM
import shutil
import json
import numpy as np
from sklearn.metrics import accuracy_score
from pystruct.learners.structured_perceptron import StructuredPerceptron
from itertools import combinations, combinations_with_replacement
from dependency_parser import dep2word, dep2ind, Node, sentence2dependencies
# import problem2sentence
import re
import logger
import ast
from utils import is_func, check_solution, clean_name, get_min_mask
import sentence2word
import problem2sentence
import string
import datetime
import CRF_struct
from CRF_struct import get_features
from CRF_struct import CrfStruct
from problem2sentence import Problem2Sentence


class Problem2Sentence_Struct(CrfStruct):
    # sentence: Return the number of different passwords Fred needs to try.
    # dependencies: ROOT-0(root=needs-8(dep=Return-1(dobj=number-3(det=the-2, prep_of=passwords-6(amod=different-5))), nsubj=Fred-7, xcomp=try-10(aux=to-9)))
    # pos: ROOT(root=V(dep=V(dobj=NN(det=article(prep_of=NNS(amod=ADJ))), nsubj=NNP, xcomp=V(aux=P)))
    # nodes: [ROOT, needs, Return,number, the, passwords, different, Fred, try, to]
    # edges: [(0,1), (1,2), ...]
    # edge_features: [root, dep,...] 
    # output: ROOT(root=O(reduce=return(reduce=len(O=O(var=possibilities(amod=set))), O=O, O=O(O=O)))
    # output: ROOT(O(reduce(reduce(O(var(reduce))), O, O(O)))
    # output: [ROOT, O, reduce, reduce, O, var, reduce, O, O, O]
    def sentence2input(self, sentence_parse):
        sentence = sentence_parse['sentence']
        sentwords = tokenize_sentences(sentence)[0]
        pos = zip(*nltk.pos_tag(sentwords))[1]
        dependencies = sentence2dependencies(sentence)[0] #TODO: check if bug
        nodes = self.get_nodes(dependencies)
        node_features = [(dep2word(n), pos[dep2ind(n)-1]) for n in nodes]
        edge_features, edge_sources, edge_targets = zip(*dependencies)
        edges = [[nodes.index(s), nodes.index(t)] for s, t in zip(edge_sources, edge_targets) if set([s,t]).issubset(set(nodes))]
          
        #TODO: clean words 
        return (node_features, edges, edge_features)
    
    # def sentence2input(sentence_parse):
    #     sentence = sentence_parse['sentence']
    #     translations = sentence_parse['translations']
    #     code = sentence_parse['code']
    #     labels = ['sentence_type'] 
    # #     labels = sentence2word.types + ['sentence_type'] 
    # #     labels = sentence2word.types
    #     dependencies = sentence2dependencies(sentence)[0] #TODO: check if bug
    #     nodes = get_nodes(dependencies)
    #     edge_features, edge_sources, edge_targets = zip(*dependencies)
    #     label_features = [[dep2word(n) for n in nodes] + list(edge_features) for label in labels] #TODO: use pos
    #     edges = [[labels.index(s), labels.index(t)] for s,t in combinations_with_replacement(labels, 2)] #TODO: fix (remove replacements)
    #     edge_features = ['O' for s,t in combinations_with_replacement(labels, 2)]
    #       
    #     #TODO: clean words
    #     #TODO: add the edges (with connected nodes) as features
    #     #TODO: config file for features 
    #     return (label_features, edges, edge_features)
    
    
    def sentence2output(self, sentence_parse, only_code=True):
        sentence = sentence_parse['sentence']
        translations = sentence_parse['translations']
        code = sentence_parse['code']
        method = sentence_parse['method']
        dependencies = sentence2dependencies(sentence)[0]
        nodes = self.get_nodes(dependencies)
        sentwords = map(dep2word, nodes)
        symbol = problem2sentence.get_type(sentence, translations, code, method)
        N = len(nodes)
        output = ['O']*N
        relevantwords = set()
        for translation,codeline in zip(translations,code):
    #         codewords = nltk.word_tokenize(codeline)
            transwords = nltk.word_tokenize(translation)
    #         if not codewords:
    #             continue
            relevantwords.update(set(sentwords) & set(transwords) - set(string.punctuation))
    #         relevantwords += [word for word in transwords if word not in string.punctuation]
        mask = get_min_mask(sentwords,relevantwords)
        output = [ symbol if mask[i] else output[i] for i in range(N)]
    #         index = mask.index(1)
    #         labels[index] = 'B'+symbol
        return output
    
    
    # def sentence2output(sentence_parse):
    #     sentence = sentence_parse['sentence']
    #     translations = sentence_parse['translations']
    #     code = sentence_parse['code']
    #     method = sentence_parse['method']
    #     sentence_type = problem2sentence.get_type(sentence, translations, code, method)
    # #     dependencies = sentence2dependencies(sentence)[0]
    # #     nodes = get_nodes(dependencies)
    #     labels = sentence2word.types
    #     N = len(labels)
    #     output = [sentence_type]
    # #     output = ['O']*N + [sentence_type]
    # #     output = ['O']*N
    # #     sentwords = nltk.word_tokenize(sentence)
    # #     for translation, codeline in zip(translations, code):
    # #         codewords = nltk.word_tokenize(codeline)
    # #         transwords = nltk.word_tokenize(translation)
    # #         label = sentence2word.get_type(codewords)
    # #         if not label:
    # #             continue
    # #         funcwords = filter(is_func, codewords)
    # #         if funcwords:
    # #             output[labels.index(label)] = funcwords[-1]
    # # #         transcodedict = dict(zip(transwords,codewords))
    # # #         word_nodes = map(dep2word, nodes)
    # # #         output = [label if n in transwords and is_func(transcodedict[n]) else o for n, o in zip(word_nodes, output)]
    # # #         output = ['var' if n in transwords and not is_func(transcodedict[n]) else o for n, o in zip(word_nodes, output)]
    # # #     if output == ['O']*N + [sentence_type]:
    # #     if output == ['O']*N:
    # #         return None 
    #     return output
    
    
    

def main():
    p2ss = Problem2Sentence_Struct()
    problem_dir = os.path.join('res', 'text&code6') 
#     problem_dir = os.path.join('res', 'small') 
    indir = problem_dir
    train_dir = os.path.join(problem_dir, 'sentence_train_struct')
    fname = 'GogoXBallsAndBinsEasy.py'
    fname = 'PalindromesCount.py'
#     struct_problem(fname, indir, outdir)
    p2ss.build_train(indir, train_dir)
    
    test_indir = os.path.join('res', 'problems_test')
    test_dir = os.path.join(test_indir,'sentence_test_struct')
#     build_train(test_indir, test_dir, False)

    outdir = os.path.join(problem_dir, 'sentence_json_struct')
    p2ss.test(train_dir, outdir, build=True)

    test_output_dir = os.path.join(test_indir, 'sentence_json_struct')
#     CRF_struct.test(train_dir, test_output_dir, test_dir=test_dir)

    n = 2
    labels = get_features(train_dir)[2]
    labels.remove('O')
    p2s = Problem2Sentence()
    print(p2s.calc_score(outdir, n))

if __name__ == '__main__':
    main()

#TODO: use part of speech for node features
#TODO: use ast as Y