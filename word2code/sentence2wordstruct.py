'''
Created on Jun 14, 2015

@author: jordan
'''
from stanford_corenlp import sentence2dependencies, tokenize_sentences
import sentence2word
import nltk
import os
from problem_parser import parse_problem
from word2codeword import is_func
import string
from pystruct.models.edge_feature_graph_crf import EdgeFeatureGraphCRF
from pystruct.learners.one_slack_ssvm import OneSlackSSVM
import shutil
import json
import numpy as np
from sklearn.metrics import accuracy_score
from pystruct.learners.structured_perceptron import StructuredPerceptron
import copy
from itertools import combinations
from dependency_parser import dep2word, dep2ind, Node
import problem2sentence
from solution_check import check_solution
import re
import logger
import ast


# sentence: Return the number of different passwords Fred needs to try.
# dependencies: ROOT-0(root=needs-8(dep=Return-1(dobj=number-3(det=the-2, prep_of=passwords-6(amod=different-5))), nsubj=Fred-7, xcomp=try-10(aux=to-9)))
# pos: ROOT(root=V(dep=V(dobj=NN(det=article(prep_of=NNS(amod=ADJ))), nsubj=NNP, xcomp=V(aux=P)))
# nodes: [ROOT, needs, Return,number, the, passwords, different, Fred, try, to]
# edges: [(0,1), (1,2), ...]
# edge_features: [root, dep,...] 
# output: ROOT(root=O(reduce=return(reduce=len(O=O(var=possibilities(amod=set))), O=O, O=O(O=O)))
# output: ROOT(O(reduce(reduce(O(var(reduce))), O, O(O)))
# output: [ROOT, O, reduce, reduce, O, var, reduce, O, O, O]
# def sentence2input(sentence_parse):
#     sentence = sentence_parse['sentence']
#     sentwords = tokenize_sentences(sentence)[0]
#     pos = zip(*nltk.pos_tag(sentwords))[1]
#     dependencies = sentence2dependencies(sentence)[0] #TODO: check if bug
#     nodes = get_nodes(dependencies)
#     print(pos)
#     print(nodes)
#     node_features = [(dep2word(n), pos[dep2ind(n)-1]) for n in nodes]
#     edge_features, edge_sources, edge_targets = zip(*dependencies)
#     edges = [[nodes.index(s), nodes.index(t)] for s, t in zip(edge_sources, edge_targets)]
#      
#     #TODO: clean words 
#     return (node_features, edges, edge_features)

def sentence2input(sentence_parse):
    sentence = sentence_parse['sentence']
    translations = sentence_parse['translations']
    code = sentence_parse['code']
#     labels = sentence2word.types + ['sentence_type'] 
    labels = sentence2word.types
    dependencies = sentence2dependencies(sentence)[0] #TODO: check if bug
    nodes = get_nodes(dependencies)
    edge_features, edge_sources, edge_targets = zip(*dependencies)
    label_features = [[dep2word(n) for n in nodes] + list(edge_features) for label in labels] #TODO: use pos
    edges = [[labels.index(s), labels.index(t)] for s,t in combinations(labels, 2)]
    edge_features = ['O' for s,t in combinations(labels, 2) ]
      
    #TODO: clean words
    #TODO: add the edges (with connected nodes) as features
    #TODO: config file for features 
    return (label_features, edges, edge_features)


# def sentence2output(sentence_parse):
#     sentence = sentence_parse['sentence']
#     translations = sentence_parse['translations']
#     code = sentence_parse['code']
#     dependencies = sentence2dependencies(sentence)[0]
#     nodes = get_nodes(dependencies)
#     N = len(nodes)
#     output = ['O']*N
#     sentwords = nltk.word_tokenize(sentence)
#     for translation, codeline in zip(translations, code):
#         codewords = nltk.word_tokenize(codeline)
#         transwords = nltk.word_tokenize(translation)
#         label = sentence2word.get_type(codewords)
#         if not label:
#             continue
#         transcodedict = dict(zip(transwords,codewords))
#         word_nodes = map(dep2word, nodes)
#         output = [label if n in transwords and is_func(transcodedict[n]) else o for n, o in zip(word_nodes, output)]
#         output = ['var' if n in transwords and not is_func(transcodedict[n]) else o for n, o in zip(word_nodes, output)]
#     if output == ['O']*N:
#         return None 
#     return output

def sentence2output(sentence_parse):
    sentence = sentence_parse['sentence']
    translations = sentence_parse['translations']
    code = sentence_parse['code']
    method = sentence_parse['method']
    sentence_type = problem2sentence.get_type(sentence, translations, code, method)
#     dependencies = sentence2dependencies(sentence)[0]
#     nodes = get_nodes(dependencies)
    labels = sentence2word.types
    N = len(labels)
#     output = ['O']*N + [sentence_type]
    output = ['O']*N
    sentwords = nltk.word_tokenize(sentence)
    for translation, codeline in zip(translations, code):
        codewords = nltk.word_tokenize(codeline)
        transwords = nltk.word_tokenize(translation)
        label = sentence2word.get_type(codewords)
        if not label:
            continue
        funcwords = filter(is_func, codewords)
        if funcwords:
            output[labels.index(label)] = funcwords[-1]
#         transcodedict = dict(zip(transwords,codewords))
#         word_nodes = map(dep2word, nodes)
#         output = [label if n in transwords and is_func(transcodedict[n]) else o for n, o in zip(word_nodes, output)]
#         output = ['var' if n in transwords and not is_func(transcodedict[n]) else o for n, o in zip(word_nodes, output)]
#     if output == ['O']*N + [sentence_type]:
    if output == ['O']*N:
        return None 
    return output


def get_nodes(dependencies):
    root = Node('ROOT-0')
    nodes = root.deps2tree(dependencies).get_nodes()
    return nodes

def struct_problem(fname, indir, outdir):
    with open(os.path.join(indir,fname),'r') as fp:
        problem = fp.read()
    parse = parse_problem(problem)
    problem_labels = {}
    problem_labels['inputs'] = []
    problem_labels['outputs'] = []    
    for sentence_parse in parse['sentences']:
        struct_output = sentence2output(sentence_parse)
        if struct_output == None:
            continue
        struct_input = sentence2input(sentence_parse)
        problem_labels['inputs'].append(struct_input)
        problem_labels['outputs'].append(struct_output)
    with open(os.path.join(outdir,fname), 'w') as fp:
        json.dump(problem_labels, fp, indent=4)
    return problem_labels

def build_train(indir, outdir):
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    os.mkdir(outdir)    
    for fname in sorted(os.listdir(indir)):
        if not fname.endswith('.py'):
            continue
        print(fname)
        problem_labels = struct_problem(fname, indir, outdir) 

def features2matrix(features, all_features):
    N = len(features)
    M = len(all_features)
#     all_features = list(all_features)
    mat = np.zeros((N, M))
    for i, feature in enumerate(features):
        if hasattr(feature, "__iter__"):
            for f in feature:
                j = all_features.index(f) 
                mat[i,j] = 1
        else:
            j = all_features.index(feature) 
            mat[i,j] = 1
    return mat

def build_features(path):
    node_features = set()
    edge_features = set()
    output_features = set()
    for fname in sorted(os.listdir(path)):
        if not fname.endswith('.py'):
            continue
        print(fname)
        with open(os.path.join(path, fname), 'r') as fp:
            fjson = json.load(fp)
        inputs = fjson['inputs']
        for (node_features_, edges_, edge_features_) in inputs:
            for f in node_features_:
                node_features |= set(f)
            edge_features |= set(edge_features_)
        for output in fjson['outputs']:
#             for f in output:
#                 output_features |= set(f)
            output_features |= set(output)
    return list(node_features), list(edge_features), list(output_features)

def get_features(path, build=False):
    features_file = os.path.join(path, 'features.json')
    if not build and os.path.exists(features_file):
        with open(features_file) as fp:
            node_features, edge_features, output_features = json.load(fp)
        return (node_features, edge_features, output_features)
    node_features, edge_features, output_features = build_features(path)
    with open(features_file, 'w') as fp:
        json.dump((node_features, edge_features, output_features), fp, indent = 4)
    return (node_features, edge_features, output_features)

def get_data(path, fname, features):
    all_node_features, all_edge_features, all_output_features = features 
    X_train = []
    Y_train = []
    X_test = []
    Y_test = []
    for fname_ in sorted(os.listdir(path)):
        if not fname_.endswith('.py'):
            continue
#         print(os.path.join(path, fname_))
        with open(os.path.join(path, fname_), 'r') as fp:
            fjson = json.load(fp)
        matrix_inputs = []
        for (node_features, edges, edge_features) in fjson['inputs']:
            node_features = features2matrix(node_features, all_node_features)
            edges = [list(edge) for edge in edges] #TODO: remove after running build train
            edges = np.array(edges)
            edge_features = features2matrix(edge_features, all_edge_features)
            matrix_inputs.append((node_features, edges, edge_features))
        matrix_outputs = []
        for output in  fjson['outputs']:
#             print(output)
#             output = features2matrix(output, all_output_features)
            output = np.array([all_output_features.index(o) for o in output])
            matrix_outputs.append(output)
        if fname_ == fname:
            X_test.extend(matrix_inputs)
            Y_test.extend(matrix_outputs)
        else:
            X_train.extend(matrix_inputs)
            Y_train.extend(matrix_outputs)
    return (X_train, Y_train, X_test, Y_test)

def output2json(model, learner, X_test, Y_test, Y_pred, features):
    (node_features, edge_features, output_features) = features
    sentences_json = []
    s = learner.score(X_test, Y_pred)
#     print(X_test)
    for i,sentence in enumerate(Y_pred):
        lines_json = []
        x = X_test[i]
        w = learner.w
        y_relaxed = model.inference(x, w, relaxed=True)
        for j,y in enumerate(sentence):
            d = {}
            d['word'] = node_features[list(X_test[i][0][j]).index(1)]
            d['prediction'] = (s, output_features[Y_pred[i][j]])
            d['label'] = output_features[Y_test[i][j]]
            if type(y_relaxed) is tuple: 
                d['probs'] = str([(y_relaxed[0][j][k], output_features[k]) for k in range(len(output_features))])
            else:
                d['probs'] = str([(float(k == Y_pred[i][j]), output_features[k]) for k in range(len(output_features))])
#             print(features)
#             print(Y_pred[i][j])
            lines_json.append(d)
        sentences_json.append(lines_json)
    return sentences_json

def test(indir, outdir, build=False):
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    os.mkdir(outdir)    
    features = get_features(indir, build)
    inference_method = 'ad3'
    crf = EdgeFeatureGraphCRF(n_states=len(features[2]), inference_method=inference_method)
    print(crf.inference_method)
#     learner = OneSlackSSVM(crf, inference_cache=50, C=.1, tol=.1, max_iter=100,
#                         n_jobs=1)
    learner = StructuredPerceptron(crf)
    for fname in sorted(os.listdir(indir)):
        if not fname.endswith('.py'):
            continue
        print(fname)
        X_train, Y_train, X_test, Y_test = get_data(indir, fname, features)
        train_states = np.unique(np.hstack([y.ravel() for y in Y_train]))
        if len(train_states) != len(features[2]):
            continue
#         print(X_train[0][0].shape)
#         print(Y_train[0].shape)
# #         for x, y in zip(X_train, Y_train):
# #             n_nodes = x[0].shape[0]
# #             y = y.reshape(n_nodes)
# #             print(y)
        learner.fit(X_train, Y_train)
        
        # Evaluate using confusion matrix.
#         Y_pred = ssvm.predict(X_test)
        Y_pred = learner.predict(X_test)
        
        output_json = output2json(crf, learner, X_test, Y_test, Y_pred, features)
        print(Y_test)
        print(Y_pred)
        if not Y_pred:
            continue
        print("weights: {}".format(learner.w))
        print("Results using only directional features for edges")
        print("Test accuracy: %.3f"
              % accuracy_score(np.hstack(Y_test), np.hstack(Y_pred)))
#         print(output_json)
        with open(os.path.join(outdir, fname), 'w') as fp:
            json.dump(output_json, fp, indent=4)


def get_label_probs(line):
    probs = ast.literal_eval(line['probs'])
    probs = sorted(probs,reverse = True)
    return probs

def get_label_words(line, label):
    label_words = []
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
#     print(total)
    if total:
        print(float(len(correct))/total)
    return correct


if __name__ == '__main__':
    problem_dir = os.path.join('res', 'text&code6') 
    indir = problem_dir
    outdir = os.path.join(problem_dir, 'word_train_struct')
    fname = 'GogoXBallsAndBinsEasy.py'
    fname = 'PalindromesCount.py'
#     struct_problem(fname, indir, outdir)
#     build_train(indir, outdir)
    indir = outdir
    outdir = os.path.join(problem_dir, 'word_json_struct')
#     test(indir, outdir, build=True)

    n = 2
    labels = get_features(indir)[2]
    labels.remove('O')
    print(sentence2word.calc_score(outdir, n, labels=labels))



#TODO: use part of speech for node features
#TODO: use ast as Y