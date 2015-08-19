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
from utils import is_func, check_solution, clean_name
import sentence2word
from CRF_struct import get_features
from CRF_struct import CrfStruct
from sentence2word import Sentence2Word


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
        

def main():
    s2ws = Sentence2WordStruct()
    problem_dir = os.path.join('res', 'text&code8') 
#     problem_dir = os.path.join('res', 'small') 
    indir = problem_dir
    train_dir = os.path.join(problem_dir, 'word_train_struct')
    fname = 'GogoXBallsAndBinsEasy.py'
    fname = 'PalindromesCount.py'
#     struct_problem(fname, indir, outdir)
#     s2ws.build_train(indir, train_dir, True)
    
    test_indir = indir
#     test_indir = os.path.join('res', 'problems_test')
    test_dir = os.path.join(test_indir,'word_test_struct')
#     s2ws.build_train(test_indir, test_dir, False)

    outdir = os.path.join(problem_dir, 'word_json_struct')
#     s2ws.test(train_dir, outdir, build_features=True, overwrite=False)
    
    test_output_dir = os.path.join(test_indir, 'word_json_test_struct')
    s2ws.test(train_dir, test_output_dir, test_dir=test_dir, overwrite=False)

    n = 2
    labels = get_features(train_dir)[2]
    labels.remove('O')
    s2w = Sentence2Word()
#     print(s2w.calc_score(outdir, n, labels=labels))
    print(s2w.calc_score(outdir, n))

if __name__ == '__main__':
    main()

#TODO: use part of speech for node features
#TODO: use ast as Y