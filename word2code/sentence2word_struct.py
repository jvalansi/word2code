'''
Created on Jun 14, 2015

@author: jordan
'''
from stanford_corenlp import tokenize_sentences
# import sentence2word
import nltk
import os
from dependency_parser import dep2word, dep2ind, Node, sentence2dependencies
# import problem2sentence
from utils import is_func, check_solution, clean_name, get_codeline_type
import sentence2word
from CRF_struct import get_features
from CRF_struct import CrfStruct
from sentence2word import Sentence2Word
import ast
import argparse


class Sentence2WordStruct(CrfStruct):
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
        edges = [[nodes.index(s), nodes.index(t)] for s, t in zip(edge_sources, edge_targets) if set([s,t]).issubset(nodes)]
          
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
        dependencies = sentence2dependencies(sentence)[0]
        nodes = self.get_nodes(dependencies)
        N = len(nodes)
        output = ['O']*N
        sentwords = nltk.word_tokenize(sentence)
        for translation, codeline in zip(translations, code):
            codewords = nltk.word_tokenize(codeline)
            transwords = nltk.word_tokenize(translation)
            label = get_codeline_type(codeline)
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
    # #     sentkwords = nltk.word_tokenize(sentence)
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
        

    
    def get_label_probs(self, sentence, label, n=None):
        '''
        get probability for the given label, for each of the words in the sentence
        
        :param sentence: sentence in json format
        :param label:
        :param n: number of possible words for each label 
        '''
        sentprobs = []
        for line in sentence:
            important = line['label'] == label
            probs = {v: k for k, v in ast.literal_eval(line['probs'])}
            if label in probs:
                prob = probs[label]
            else:
                prob = 0
            sentprobs.append((prob,important,line['word'],sentence.index(line)))
        sentprobs = sorted(sentprobs,reverse = True)
        return sentprobs[:n]


def main():
    problem_dir = os.path.join('res', 'text&code8', 'solutions', 'AverageAverage', 'Good') 
    problem_dir = os.path.join('res', 'text&code8') 
#     problem_dir = os.path.join('res', 'small') 

    parser = argparse.ArgumentParser()
    parser.add_argument("-pd","--problem_dir", help="Directory of the problems to be labeled",
                        default=problem_dir)
    parser.add_argument("-td", "--train_dir", help="Directory of the labeled problems")
    parser.add_argument("-od", "--outdir", help="Directory to store output")
    parser.add_argument("-m", "--M", help="Top M words allowed per label", type=int, default=3)
    parser.add_argument("-a", "--all", help="Whether to label all the sentences or only the ones with code", action="store_true")
    parser.add_argument("-o", "--online", help="Whether to test online", action="store_true")
    parser.add_argument("-jd", "--json_dir", help="Directory of labeled problems for online")
    parser.add_argument("-sd", "--solution_dir", help="Directory of problem solutions for online")
    args = parser.parse_args()

    
    s2ws = Sentence2WordStruct()
    indir = args.problem_dir
    only_code = not args.all
    if not args.train_dir:
        args.train_dir = os.path.join(problem_dir, 'word_train_struct')
    s2ws.build_train(indir, args.train_dir, only_code)
    
    if not args.outdir:
        args.outdir = os.path.join(problem_dir, 'word_json_struct')
    s2ws.test(args.train_dir, args.outdir, build_features=True, overwrite=True, 
              online=args.online, json_dir=args.json_dir, sol_dir=args.solution_dir)
    
    labels = get_features(args.train_dir)[2]
    labels.remove('O')
    s2w = Sentence2Word()
    print(s2w.calc_score(args.outdir, args.M, labels=labels))
#     result1 = s2w.calc_score(outdir, n)
#     online_dir = outdir+'_online'
#     result2 = s2w.calc_score(online_dir, n)
#     print(set(result2).difference(set(result1)))

    fname = 'GogoXBallsAndBinsEasy.py'
    fname = 'PalindromesCount.py'
#     struct_problem(fname, indir, outdir)


if __name__ == '__main__':
    main()

#TODO: use part of speech for node features
#TODO: use ast as Y