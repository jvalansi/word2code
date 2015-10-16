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
from itertools import combinations, combinations_with_replacement, product
from dependency_parser import dep2word, dep2ind, Node, sentence2dependencies
# import problem2sentence
import re
import logger
import ast
from utils import is_func, check_solution, clean_name
from learner_wrapper import LearnerWrapper
import online_learning
from online_learning import online_learn, online_update_from_examples
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
        nodes = Node('ROOT-0').deps2tree(dependencies).get_nodes()
        return nodes
    
    def label_problem(self, indir, fname, outdir=None, only_code=False):
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
        if outdir:
            with open(os.path.join(outdir,clean_name(fname)+'.label'), 'w') as fp:
                json.dump(problem_labels, fp, indent=4)
        return problem_labels

    
    def labels2output(self, all_output_features, output):
        return np.array([all_output_features.index(o) for o in output])
    
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
            output = self.labels2output(all_output_features, output)
            matrix_outputs.append(output)
        return matrix_inputs, matrix_outputs
    
    def get_data(self, train_dir, fname, features, test_dir=None):#TODO: split to train, test
        X_train = []
        Y_train = []
        X_test = []
        Y_test = []
        if not test_dir:
            test_dir = train_dir
            test_fnames = [fname]
        else:
            test_fnames = sorted(os.listdir(test_dir)) 
        train_fnames = sorted(os.listdir(train_dir))
        if fname in train_fnames:
            train_fnames.remove(fname)
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
                if type(y_relaxed) is tuple: 
                    d['probs'] = str([(y_relaxed[0][j][k], output_features[k]) for k in range(len(output_features))])
                else:
                    d['probs'] = str([(float(k == Y_pred[i][j]), output_features[k]) for k in range(len(output_features))])
                lines_json.append(d)
            sentences_json.append(lines_json)
        return sentences_json
    
    def get_probable_Y(self, fpath_json, output_features, n):
        Y = []
        with open(fpath_json, 'r') as inputjson:
            problem_json = json.load(inputjson)
        for sentence in problem_json:
#         get probable labels
            y = ['O']*len(sentence)
            for label in output_features:
                label_idx = self.get_label_probs(sentence, label, n)
                y = [label if i in label_idx else y for i,y in enumerate(y)]
#         use probable labels to generate Y
            y = self.labels2output(output_features, y)
            Y.append(y)
        return Y
    
    def build_and_get_data(self, data_dir):
        Xs = []
        Ys = []
        self.build_train(data_dir, data_dir)
        data_features = get_features(data_dir)
        for sol_fname in os.listdir(data_dir):
            if not sol_fname.endswith('.label'):
                continue
            (X_data, Y_data) = self.get_data_from_file(data_dir, sol_fname, data_features)
            Xs.append(X_data)
            Ys.append(Y_data)
        return (Xs, Ys)
    
    def test_file(self, train_dir, fname, features, learner, model, outdir, 
                  test_dir=None, overwrite=True, online=False, n=2, json_dir=None, sol_dir=None):
        fpath_out = os.path.join(outdir, clean_name(fname)+'.json')
        if not overwrite and os.path.exists(fpath_out):
            return
        X_train, Y_train, X_test, Y_test = self.get_data(train_dir, fname, features, test_dir)
        (node_features, edge_features, output_features) = features
        if online and json_dir:
            #TODO: only if correct
            #    get the probable Y which solves the problem
            fpath_json = os.path.join(json_dir, clean_name(fname)+'.json')
            probable_Y = self.get_probable_Y(fpath_json, output_features, n)
            
            X_train.extend(X_test)
            Y_train.extend(probable_Y)
            
        train_states = np.unique(np.hstack([y.ravel() for y in Y_train]))
        if len(train_states) != len(output_features):
            return
        print(X_train[0][0].shape)
        print(Y_train[0].shape)
        print(len(X_train))
        print(len(Y_train))
# #         for x, y in zip(X_train, Y_train):
# #             n_nodes = x[0].shape[0]
# #             y = y.reshape(n_nodes)
# #             print(y)

        learner.fit(X_train, Y_train)
        
        if online and sol_dir:  
            # get all Y_goods from good folder
            # for each Y_good get most similar Y_bads
            # for each pair of Y_good, Y_bad update learner
            good_dir = os.path.join(sol_dir, 'Good')
            X_goods, Y_goods = self.build_and_get_data(good_dir)
            bad_dir = os.path.join(sol_dir, 'Bad')
            X_bads, Y_bads = self.build_and_get_data(bad_dir)
            pairs = {}
            for (Y_good,Y_bad) in product(Y_goods,Y_bads):
                if Y_good not in pairs or pairs[Y_good] > learner.model.loss(Y_good, Y_bad): #TODO: check >
                    pairs[Y_good] = learner.model.loss(Y_good, Y_bad)
            effective_lr = (learner.max_iter+learner.decay_t0)**learner.decay_exponent
            for Y_good, Y_bad in pairs.items():
                learner = online_update_from_examples(X_test, Y_good, Y_good, learner, 0, effective_lr)
        
        # Evaluate using confusion matrix.
        Y_pred = learner.predict(X_test)
        if not Y_pred:
            return

        output_json = self.output2json(model, learner, X_test, Y_test, Y_pred, features)
        with open(fpath_out, 'w') as fp:
            json.dump(output_json, fp, indent=4)

        print("weights: {}".format(learner.w))
        print("Results using only directional features for edges")
        print("Test accuracy: %.3f"
              % accuracy_score(np.hstack(Y_test), np.hstack(Y_pred)))

    
    def test(self, train_dir, outdir, test_dir=None, build_features=False, overwrite=True, 
             online=False, n=2, json_dir=None, sol_dir=None):
        if os.path.exists(outdir) and overwrite:
            shutil.rmtree(outdir)
        if not os.path.exists(outdir):
            os.mkdir(outdir)    
        features = get_features(train_dir, build_features)
        inference_method = 'ad3'
        inference_method = 'lp'
#         inference_method = None
        crf = EdgeFeatureGraphCRF(n_states=len(features[2]), inference_method=inference_method)
        print(crf.inference_method)
    #     learner = OneSlackSSVM(crf, inference_cache=50, C=.1, tol=.1, max_iter=100,
    #                         n_jobs=1)
        n_jobs = 3
        n_jobs = 1
        learner = StructuredPerceptron(crf, batch=True, n_jobs=n_jobs)
#         learner = StructuredPerceptron(crf)
        for fname in sorted(os.listdir(train_dir)):
            if not fname.endswith('.label'):
                continue
            print(datetime.now())
            print(fname)
            self.test_file(train_dir, fname, features, learner, crf, outdir, test_dir, overwrite, 
                           online=online, n=2, json_dir=json_dir, sol_dir=sol_dir)
    
    

if __name__ == '__main__':
    pass

#TODO: use ast as Y

#TODO: use good vs. bad examples for learning 