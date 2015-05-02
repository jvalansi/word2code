'''
Created on Dec 3, 2014

@author: jordan
'''
import nltk
from nltk import word_tokenize
from nltk.corpus import conll2000
from autotag.autotag import AutoTag
import sentence_parser
import json
import os
import probability_calc

def tree2string(tree):
    s = ""
    for key,val in tree:
        s += '"'+key+'"'
        if isinstance(val,dict):
            s += '{'
            s += tree2string(val)
            s += '}'
        else:
            s += ':'+'"'+str(val)+'"'
        s += ','
    return s


def tree2code(tree):
    s = ""
    # walk tree, depth first
    # [('ROOT', 
    #    [('S', 
    #        [('VP', 
    #            [('VB', 'return'), 
    #            ('NP', 
    #                [('NP', [('DT', 'the'), ('NN', 'number')]), 
    #                ('PP', 
    #                    [('IN', 'of'), 
    #                    ('NP', [('JJ', 'different'), ('NNS', 'passwords')]
    #                )]
    #            )]
    #        )]), 
    #        ('.', '.')]
    #    )]
    # )]
    # (non_terminal, terminal) -> terminal
    # (non_terminal, X, X) -> terminal(terminal)
    print(tree)
    if (tree[0] == ('DT', 'the') or tree[0][0] == 'IN') :
        tree = tree[1:]
    if len(tree[0]) < 2: #terminal
        return tree
    
    s += tree2code(tree[0][1])
    args = []
    for i in range(1,len(tree)):
        if tree[i][1] == '.':
            continue
        args.append(tree2code(tree[i][1]))
    if args:
        s += '('+','.join(args)+')'
    return s

def get_data(dir):
    data = []
    sp = sentence_parser.SentenceParser()
    at = AutoTag()
    entry = Entry(None,"",[])
    for file in os.listdir(dir):
        with open(dir+file,'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if line.startswith('#'):
                    data.append(entry)
                    sentence = line[1:] 
                    sentence = at.clean_text(sentence)
#                     parse = sp.parse_sentence(sentence)
#                     tree = parse[0][0]
#                     sentence = tree2string(tree)
#                     relations = parse[0][1]
#                     sentence = ' '.join([r[0]+' '+r[1][0] + ' ' + r[1][1] for r in relations])
                    entry = Entry(None,sentence,[],"")
                else:
#                     entry.tags.append(line)
                    entry.code += line
#    for each file:
#        a sentence starts with #
#        if the is a non sentence after a sentence it is it's tag
    return(data)

class Entry:
    def __init__(self,eid = None,text = "",tags = [], code = ""):
        if eid is None:
            eid = id(self)
        self.id = eid
        self.text = text
        self.tags = tags
        self.code = code 

class TopCoderSolver:
    
    def tag_sentence(self,sentence):
#         train on 
        pass
    
    def get_imperative(self,parses):
        print('getting imperative')
        for (tree,relations) in parses:
#             if 'S' in tree['ROOT']:
#                 keys =  tree['ROOT']['S'].keys()
#                 if 'VP' in keys and 'NP' not in keys:
#                     return (tree,relations)
            if 'return' in tree2string(tree).lower():
                return (tree,relations)
    
    def get_condition(self,parse_trees):
        #TODO: 
        pass
    
    def get_mapping(self,parse_trees):
        #TODO: 
        pass 
    
    def get_permutations(self,parse_trees):
        #TODO:
        pass
    
    def parse_problem(self, problem):
        sp = sentence_parser.SentenceParser()
        return sp.parse_file(problem)
        
        # get problem data
    def get_data(self):

        #TODO: 
        pass
    
    def solve(self,problem):
        # extract parse tree
        parses = self.parse_problem(problem)
        #  
        # find imperative (return something)
        (tree,relations) = self.get_imperative(parses)
        print(tree)
        code = tree2code(tree)
        print(code)
        # find condition (for reduce)
        condition = self.get_condition(parses) 
        # find mapping
        mapping = self.get_mapping(parses)
        # find all possible permutations
        permutaions = self.get_permutations(parses)
        
        

if __name__ == '__main__':
    data = get_data('res/text&code/')
    coocurences = probability_calc.calc_cooccurences(data)
    print(coocurences[('return','min')])

#     N = len(data)
#     print(N)
#     at = AutoTag()
#     at.classify(data[:N/2])
#     at.test(data[N/2+1:])
#     sentence = data[11] 
#     print(sentence.text)
#     print(at.test_doc(data[11], ['Return','Valid','Map'], 0))

#     tcs = TopCoderSolver()
#     print(tcs.solve('res/return'))
    
#     parser_out = os.popen("~/Downloads/stanford-parser-full-2014-08-27/lexparser.sh res/sentences").readlines()
#     
#     parse_list = parse2list(parser_out)
#     for parse0,parse1 in parse_list: 
#         parse0 = re.sub("\s+", " ",parse0)
# #         print(parse0)
#         parse_tree = parse2tree(parse0)
#         print(parse_tree)
#         parse_lambda = parse2lambda(parse_tree)
# #         print(len(parse_lambda))
#         parse1 = parse1.split('\n') 
#         relations = parse2relations(parse1)
#         for r in relations:
#             print(relation2string(r))
# #     print(parse_lambda)
    
