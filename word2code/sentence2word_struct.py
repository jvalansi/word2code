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
from utils import is_func, check_solution, clean_name
import sentence2word
import problem2sentence
import CRF_struct
from CRF_struct import get_features


# sentence: Return the number of different passwords Fred needs to try.
# dependencies: ROOT-0(root=needs-8(dep=Return-1(dobj=number-3(det=the-2, prep_of=passwords-6(amod=different-5))), nsubj=Fred-7, xcomp=try-10(aux=to-9)))
# pos: ROOT(root=V(dep=V(dobj=NN(det=article(prep_of=NNS(amod=ADJ))), nsubj=NNP, xcomp=V(aux=P)))
# nodes: [ROOT, needs, Return,number, the, passwords, different, Fred, try, to]
# edges: [(0,1), (1,2), ...]
# edge_features: [root, dep,...] 
# output: ROOT(root=O(reduce=return(reduce=len(O=O(var=possibilities(amod=set))), O=O, O=O(O=O)))
# output: ROOT(O(reduce(reduce(O(var(reduce))), O, O(O)))
# output: [ROOT, O, reduce, reduce, O, var, reduce, O, O, O]
def sentence2input(sentence_parse):
    sentence = sentence_parse['sentence']
    sentwords = tokenize_sentences(sentence)[0]
    pos = zip(*nltk.pos_tag(sentwords))[1]
    dependencies = sentence2dependencies(sentence)[0] #TODO: check if bug
    nodes = get_nodes(dependencies)
    print(pos)
    print(nodes)
    node_features = [(dep2word(n), pos[dep2ind(n)-1]) for n in nodes]
    edge_features, edge_sources, edge_targets = zip(*dependencies)
    print(nodes)
    print(edge_sources)
    print(edge_targets)
    edges = [[nodes.index(s), nodes.index(t)] for s, t in zip(edge_sources, edge_targets) if [s,t] in nodes]
      
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


def sentence2output(sentence_parse, only_code=True):
    sentence = sentence_parse['sentence']
    translations = sentence_parse['translations']
    code = sentence_parse['code']
    dependencies = sentence2dependencies(sentence)[0]
    nodes = get_nodes(dependencies)
    N = len(nodes)
    output = ['O']*N
    sentwords = nltk.word_tokenize(sentence)
    for translation, codeline in zip(translations, code):
        codewords = nltk.word_tokenize(codeline)
        transwords = nltk.word_tokenize(translation)
        label = sentence2word.get_type(codewords)
        if not label:
            continue
        transcodedict = dict(zip(transwords,codewords))
        word_nodes = map(dep2word, nodes)
        output = [label if n in transwords and is_func(transcodedict[n]) else o for n, o in zip(word_nodes, output)]
        output = ['var' if n in transwords and not is_func(transcodedict[n]) else o for n, o in zip(word_nodes, output)]
    if only_code and output == ['O']*N:
        return None 
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


def get_nodes(dependencies):
    root = Node('ROOT-0')
    nodes = root.deps2tree(dependencies).get_nodes()
    return nodes

def struct_problem(fname, indir, outdir, only_code=True):
    with open(os.path.join(indir,fname),'r') as fp:
        problem = fp.read()
    parse = parse_problem(problem)
    problem_labels = {}
    problem_labels['inputs'] = []
    problem_labels['outputs'] = []    
    for sentence_parse in parse['sentences']:
        struct_output = sentence2output(sentence_parse, only_code)
        if struct_output == None:
            continue
        struct_input = sentence2input(sentence_parse)
        problem_labels['inputs'].append(struct_input)
        problem_labels['outputs'].append(struct_output)
    with open(os.path.join(outdir,fname), 'w') as fp:
        json.dump(problem_labels, fp, indent=4)
    return problem_labels

def build_train(indir, outdir, only_code=True):
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    os.mkdir(outdir)    
    for fname in sorted(os.listdir(indir)):
        if not fname.endswith('.py'):
            continue
        print(fname)
        problem_labels = struct_problem(fname, indir, outdir, only_code) 


def get_label_probs(line):
    probs = ast.literal_eval(line['probs'])
    probs = sorted(probs,reverse = True)
    return probs

def get_label_words(line, label):
    return line['label']
    
def check_type(line, word_type, n):
    print(word_type)
    probs = get_label_probs(line)
    print(probs)
    probable_codewords = zip(*probs[:n])[-1]
    print('probable_codewords')
    print(probable_codewords)
    label_word = line['label']
    print('label_word')
    print(label_word)
    result = label_word in probable_codewords
#     result = all([not important for (sentprob,important,word) in sentprobs[n:]])
    if not result:
        logger.logging.info(word_type)
        logger.logging.info(probs)
    return result

def check_problem(json_dir,fname,n):
    with open(os.path.join(json_dir,fname),'r') as inputjson:
        problem_json = json.load(inputjson)
#     for problem in problems_json:
    problem_result = []
    for sentence in problem_json:
#         check if n most probable mappings contain all mappings
        for i, line in enumerate(sentence):
            word_type = sentence2word.types[i]
            result = check_type(line,word_type, n)
            problem_result.append(result)
#         result = check_type(sentence, 'var', n)
#         problem_result.append(result)
    return problem_result

def calc_score(json_dir, n, problem_dir=None):
    correct = []
#     no_sol = []
    total = 0
    fnames = sorted(os.listdir(json_dir))
    for fname in fnames:
        if problem_dir and not check_solution(os.path.join(problem_dir, re.sub('.label', '.py', fname))):
#             no_sol.append(fname)
            continue
        problem_result = check_problem(json_dir, fname, n)
        if any(problem_result) and all(problem_result):
            correct.append(fname)
        else:
            logger.logging.info(fname)
        total += any(problem_result)
    print(total)
    if total:
        print(float(len(correct))/total)
    return correct

def main():
    problem_dir = os.path.join('res', 'text&code6') 
    indir = problem_dir
    train_dir = os.path.join(problem_dir, 'word_train_struct')
    fname = 'GogoXBallsAndBinsEasy.py'
    fname = 'PalindromesCount.py'
#     struct_problem(fname, indir, outdir)
#     build_train(indir, train_dir)
    
    test_indir = os.path.join('res', 'problems_test')
    test_dir = os.path.join(test_indir,'word_test_struct')
#     build_train(test_indir, test_dir, False)

    outdir = os.path.join(problem_dir, 'word_json_struct')
#     CRF_struct.test(train_dir, outdir, build=True)
    test_output_dir = os.path.join(test_indir, 'word_json_struct')
    CRF_struct.test(train_dir, test_output_dir, test_dir=test_dir)

    n = 1
    labels = get_features(train_dir)[2]
    labels.remove('O')
#     print(sentence2word.calc_score(outdir, n))

if __name__ == '__main__':
    main()

#TODO: use part of speech for node features
#TODO: use ast as Y