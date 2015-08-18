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
from learner_wrapper import LearnerWrapper
import online_learning
from online_learning import online_learn
from datetime import datetime


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
        if not fname.endswith('.label'):
            continue
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

class CrfStruct(LearnerWrapper):
    
    def get_nodes(self, dependencies):
        root = Node('ROOT-0')
        nodes = root.deps2tree(dependencies).get_nodes()
        return nodes
    
    def label_problem(self, indir, fname, outdir, only_code=False):
        with open(os.path.join(indir,fname),'r') as fp:
            problem = fp.read()
        parse = parse_problem(problem)
        problem_labels = {}
        problem_labels['inputs'] = []
        problem_labels['outputs'] = []    
        for sentence_parse in parse['sentences']:
            struct_output = self.sentence2output(sentence_parse, only_code)
            if struct_output == None:
                continue
            struct_input = self.sentence2input(sentence_parse)
            problem_labels['inputs'].append(struct_input)
            problem_labels['outputs'].append(struct_output)
        with open(os.path.join(outdir,clean_name(fname)+'.label'), 'w') as fp:
            json.dump(problem_labels, fp, indent=4)
        return problem_labels

    
    def get_data_from_file(self, train_dir, fname_, features):
        with open(os.path.join(train_dir, fname_), 'r') as fp:
            fjson = json.load(fp)
        all_node_features, all_edge_features, all_output_features = features 
        matrix_inputs = []
        for (node_features, edges, edge_features) in fjson['inputs']:
            node_features = features2matrix(node_features, all_node_features)
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
    
    def get_data(self, train_dir, fname, features, test_dir=None):#TODO: split to train, test
        X_train = []
        Y_train = []
        X_test = []
        Y_test = []
        if not test_dir:
            test_dir = train_dir
        train_fnames = sorted(os.listdir(train_dir))
        if fname in train_fnames:
            train_fnames.remove(fname)
        test_fnames = [fname]            
        for fname_ in train_fnames:
            if not fname_.endswith('.label'):
                continue
            matrix_inputs, matrix_outputs = self.get_data_from_file(train_dir, fname_, features)
            X_train.extend(matrix_inputs)
            Y_train.extend(matrix_outputs)
        for fname_ in test_fnames:
            if not fname_.endswith('.label'):
                continue
            matrix_inputs, matrix_outputs = self.get_data_from_file(test_dir, fname_, features)
            X_test.extend(matrix_inputs)
            Y_test.extend(matrix_outputs)
        return (X_train, Y_train, X_test, Y_test)
    
    def output2json(self, model, learner, X_test, Y_test, Y_pred, features):
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
                if 1 in list(X_test[i][0][j]):
                    idxs = [idx for idx, v in enumerate(X_test[i][0][j]) if v == 1]
                    for idx in idxs:
                        d['word'] = node_features[idx]
                        if d['word'] != d['word'].upper():
                            break #isn't pos
                else:
                    d['word'] = 'None'
                d['prediction'] = (s, output_features[Y_pred[i][j]])
                d['label'] = output_features[Y_test[i][j]]
#                 if type(y_relaxed) is tuple: 
                d['probs'] = str([(y_relaxed[0][j][k], output_features[k]) for k in range(len(output_features))])
#                 else:
#                     d['probs'] = str([(float(k == Y_pred[i][j]), output_features[k]) for k in range(len(output_features))])
                lines_json.append(d)
            sentences_json.append(lines_json)
        return sentences_json
    
    def test_file(self, train_dir, fname, features, learner, model, outdir, test_dir=None, overwrite=True):
        fpath_json = os.path.join(outdir, clean_name(fname)+'.json')
        if not overwrite and os.path.exists(fpath_json):
            return
        X_train, Y_train, X_test, Y_test = self.get_data(train_dir, fname, features, test_dir)
        train_states = np.unique(np.hstack([y.ravel() for y in Y_train]))
        if len(train_states) != len(features[2]):
            return
        print(X_train[0][0].shape)
        print(Y_train[0].shape)
        print(len(X_test))
        print(len(Y_test))
# #         for x, y in zip(X_train, Y_train):
# #             n_nodes = x[0].shape[0]
# #             y = y.reshape(n_nodes)
# #             print(y)

        learner.fit(X_train, Y_train)
#         learner = online_learn(X_train, Y_train, learner)
        
        # Evaluate using confusion matrix.
        Y_pred = learner.predict(X_test)
        
        output_json = self.output2json(model, learner, X_test, Y_test, Y_pred, features)
#         print(Y_test)
#         print(Y_pred)
        if not Y_pred:
            return
        print("weights: {}".format(learner.w))
        print("Results using only directional features for edges")
        print("Test accuracy: %.3f"
              % accuracy_score(np.hstack(Y_test), np.hstack(Y_pred)))
        with open(fpath_json, 'w') as fp:
            json.dump(output_json, fp, indent=4)
    
    def test(self, train_dir, outdir, test_dir=None, build_features=False, overwrite=True):
        if os.path.exists(outdir) and overwrite:
            shutil.rmtree(outdir)
        if not os.path.exists(outdir):
            os.mkdir(outdir)    
        features = get_features(train_dir, build_features)
        inference_method = 'ad3'
        inference_method = 'lp'
        crf = EdgeFeatureGraphCRF(n_states=len(features[2]), inference_method=inference_method)
        print(crf.inference_method)
    #     learner = OneSlackSSVM(crf, inference_cache=50, C=.1, tol=.1, max_iter=100,
    #                         n_jobs=1)
        learner = StructuredPerceptron(crf, batch=True, n_jobs=3)
#         learner = StructuredPerceptron(crf)
        for fname in sorted(os.listdir(train_dir)):
            if not fname.endswith('.label'):
                continue
            print(datetime.now())
            print(fname)
            self.test_file(train_dir, fname, features, learner, crf, outdir, test_dir, overwrite)
    
    

if __name__ == '__main__':
    pass

#TODO: use part of speech for node features
#TODO: use ast as Y