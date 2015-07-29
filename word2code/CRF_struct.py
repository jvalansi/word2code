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

def features2matrix(features, all_features):
    N = len(features)
    M = len(all_features)
#     all_features = list(all_features)
    mat = np.zeros((N, M))
    for i, feature in enumerate(features):
        if hasattr(feature, "__iter__"):
            for f in feature:
                if f not in all_features: #TODO: think whether to fix
                    continue
                j = all_features.index(f) 
                mat[i,j] = 1
        else:
            if feature not in all_features: #TODO: think whether to fix
                continue
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
            print(os.path.join(path, fname))
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

def get_data_from_file(train_dir, fname_, features):
    with open(os.path.join(train_dir, fname_), 'r') as fp:
        fjson = json.load(fp)
    all_node_features, all_edge_features, all_output_features = features 
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
    return matrix_inputs, matrix_outputs

def get_data(train_dir, fname, features, test_dir=None):
    X_train = []
    Y_train = []
    X_test = []
    Y_test = []
    for fname_ in sorted(os.listdir(train_dir)):
        if not fname_.endswith('.py'):
            continue
#         print(os.path.join(path, fname_))
        matrix_inputs, matrix_outputs = get_data_from_file(train_dir, fname_, features)
        if not test_dir and fname_ == fname:
            X_test.extend(matrix_inputs)
            Y_test.extend(matrix_outputs)
        else:
            X_train.extend(matrix_inputs)
            Y_train.extend(matrix_outputs)
    if bool(test_dir):
        for fname_ in sorted(os.listdir(test_dir)):
            if not fname_.endswith('.py'):
                continue
            matrix_inputs, matrix_outputs = get_data_from_file(test_dir, fname_, features)
            X_test.extend(matrix_inputs)
            Y_test.extend(matrix_outputs)
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

def test(train_dir, outdir, test_dir=None, build=False):
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    os.mkdir(outdir)    
    features = get_features(train_dir, build)
    inference_method = 'ad3'
    crf = EdgeFeatureGraphCRF(n_states=len(features[2]), inference_method=inference_method)
    print(crf.inference_method)
#     learner = OneSlackSSVM(crf, inference_cache=50, C=.1, tol=.1, max_iter=100,
#                         n_jobs=1)
    learner = StructuredPerceptron(crf)
    for fname in sorted(os.listdir(train_dir)):
        if not fname.endswith('.py'):
            continue
        print(fname)
        X_train, Y_train, X_test, Y_test = get_data(train_dir, fname, features, test_dir)
        train_states = np.unique(np.hstack([y.ravel() for y in Y_train]))
        if len(train_states) != len(features[2]):
            continue
        print(X_train[0][0].shape)
        print(Y_train[0].shape)
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
        with open(os.path.join(outdir, clean_name(fname)+'.label'), 'w') as fp:
            json.dump(output_json, fp, indent=4)


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
#     test(train_dir, outdir, build=True)
    test_output_dir = os.path.join(test_indir, 'word_json_struct')
    test(train_dir, test_output_dir, test_dir=test_dir)

    n = 1
    labels = get_features(train_dir)[2]
    labels.remove('O')
#     print(sentence2word.calc_score(outdir, n))

if __name__ == '__main__':
    main()

#TODO: use part of speech for node features
#TODO: use ast as Y