'''
Created on Jun 14, 2015

@author: jordan
'''
from stanford_corenlp import sentence2dependencies
from codeline_gen_dep import Node, dep2word
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
    translations = sentence_parse['translations']
    code = sentence_parse['code']
    dependencies = sentence2dependencies(sentence)[0] #TODO: check if bug
    nodes = get_nodes(dependencies)
    node_features = [dep2word(n) for n in nodes] #TODO: use pos
#     node_features = features2matrix(nodes, all_node_features)
    edge_features, edge_sources, edge_targets = zip(*dependencies)
    edges = [[nodes.index(s), nodes.index(t)] for s, t in zip(edge_sources, edge_targets)]
#     edge_features = features2matrix(edge_features, all_edge_features)
    
    #TODO: clean words 
    return (node_features, edges, edge_features)

def sentence2output(sentence_parse):
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
    if output == ['O']*N:
        return None 
    return output

def get_nodes(dependencies):
    root = Node('ROOT-0')
    nodes = root.deps2tree(dependencies).get_nodes()
    return nodes

def struct_problem(problem):
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
    return problem_labels

def build_train(indir, outdir):
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    os.mkdir(outdir)    
    for fname in sorted(os.listdir(indir)):
        print(fname)
        with open(os.path.join(indir,fname),'r') as fp:
            problem = fp.read()
        problem_labels = struct_problem(problem) 
        with open(os.path.join(outdir,fname), 'w') as fp:
            json.dump(problem_labels, fp, indent=4)

def features2matrix(features, all_features):
    N = len(features)
    M = len(all_features)
#     all_features = list(all_features)
    mat = np.zeros((N, M))
    for i, feature in enumerate(features):
        j = all_features.index(feature) 
        mat[i,j] = 1
    return mat

def get_features(path):
    features_file = 'res/features.json'
    if os.path.exists(features_file):
        with open(features_file) as fp:
            node_features, edge_features, output_features = json.load(fp)
        return (node_features, edge_features, output_features)
    node_features = set()
    edge_features = set()
    output_features = set()
    for fname in os.listdir(path):
        print(fname)
        with open(os.path.join(path, fname), 'r') as fp:
            fjson = json.load(fp)
        inputs = fjson['inputs']
        for (node_features_, edges_, edge_features_) in inputs:
            node_features |= set(node_features_)
            edge_features |= set(edge_features_)
        for output in fjson['outputs']:
            output_features |= set(output)
    node_features, edge_features, output_features = list(node_features), list(edge_features), list(output_features)
    with open(features_file, 'w') as fp:
        json.dump((node_features, edge_features, output_features), fp, indent = 4)
    return node_features, edge_features, output_features

def get_data(path, fname, features):
    all_node_features, all_edge_features, all_output_features = features 
    X_train = []
    Y_train = []
    X_test = []
    Y_test = []
    for fname_ in sorted(os.listdir(path)):
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
#             output = features2matrix(output, ['O', 'var']+sentence2word.types)
            output = np.array([all_output_features.index(o) for o in output])
            matrix_outputs.append(output)
        if fname_ == fname:
            X_test.extend(matrix_inputs)
            Y_test.extend(matrix_outputs)
        else:
            X_train.extend(matrix_inputs)
            Y_train.extend(matrix_outputs)
    return (X_train, Y_train, X_test, Y_test)

def test(indir, outdir):
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    os.mkdir(outdir)    
    features = get_features(indir)
    crf = EdgeFeatureGraphCRF(n_states=len(features[2]))
#     ssvm = OneSlackSSVM(crf, inference_cache=50, C=.1, tol=.1, max_iter=100,
#                         n_jobs=1)
    sp = StructuredPerceptron(crf)
    for fname in sorted(os.listdir(indir)):
        X_train, Y_train, X_test, Y_test = get_data(indir, fname, features)
#         n_states = np.unique(np.hstack([y.ravel() for y in Y_train]))
#         print(n_states)
#         n_states = np.unique(np.hstack([y.ravel() for y in Y_test]))
#         print(n_states)        
#         print(X_train[0][0].shape)
#         print(Y_train[0].shape)
# #         for x, y in zip(X_train, Y_train):
# #             n_nodes = x[0].shape[0]
# #             y = y.reshape(n_nodes)
# #             print(y)
#         ssvm.fit(X_train, Y_train)
        sp.fit(X_train, Y_train)
        
        # Evaluate using confusion matrix.
#         Y_pred = ssvm.predict(X_test)
        Y_pred = sp.predict(X_test)
        print(Y_test)
        print(Y_pred)
        if not Y_pred:
            continue
        print("weights: {}".format(sp.w))
        print("Results using only directional features for edges")
        print("Test accuracy: %.3f"
              % accuracy_score(np.hstack(Y_test), np.hstack(Y_pred)))
        with open(os.path.join(outdir, fname), 'w') as fp:
            json.dump([y.tolist() for y in Y_pred], fp, indent=4)


if __name__ == '__main__':
    indir = 'res/text&code5'
    outdir = 'res/word_train_struct'
    fname = 'GogoXBallsAndBinsEasy.py'
#     with open(os.path.join(indir,fname)) as fp:
#         problem = fp.read()
#     label_problem(problem)
#     build_train(indir, outdir)
    indir = outdir
    outdir = 'res/word_test_struct'
    test(indir, outdir)


#TODO: use part of speech for node features