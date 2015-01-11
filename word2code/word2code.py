'''
Created on Dec 3, 2014

@author: jordan
'''
import nltk
from nltk import word_tokenize
from nltk.corpus import conll2000
import os
import re
import collections

WORD = '[\w\-,\=\']+'

def parse2list(parse):
    parse = "".join(parse)
    parse_list = parse.split('\n\n')
    parse_list = [(parse_list[2*i],parse_list[2*i+1]) for i in range(len(parse_list)/2) ]
    return parse_list

def get_parentheses(parse):
    depth = 0
    for i in range(len(parse)):
        if parse[i] == '(':
            depth += 1
        if parse[i] == ')':
            depth -= 1
        if depth == 0:
            return parse[:i+1]
    return None

def parse2tree(parse):
#     get string surrounded by parenthesis return dictionary
#    input: (NAME (NAME VALUE) (NAME VALUE)) 
#    output: {"NAME": {"NAME": VALUE, "NAME": VALUE}}
#     print(parse)
    if parse[0] != '(':
        return parse.split(')')[0] #return VALUE
    d = []
    while len(parse) > 0:    
        parentheses = get_parentheses(parse)
        parse = parse[len(parentheses):].strip()
        parentheses = parentheses[1:-1] #remove parentheses
        name = parentheses.split()[0]
        value = parse2tree(parentheses[len(name):].strip())
        d.append((name, value))
    return d


def parse2lambda(parse):
    if not isinstance(parse, dict):
        return parse
    lmbd = ''
    if len(parse) == 1:
        lmbd = parse.keys()[0]
        parse = parse[lmbd]
        result = lmbd+'('+ str(parse2lambda(parse)) + ')'
        return result
    if len(parse) >= 2:
        lmbd = parse.keys()
        lmbd1 = lmbd.pop(1)
        parse = parse[lmbd1]
        result = lmbd1+'('+ ','.join(lmbd)+','+str(parse2lambda(parse)) + ')'    
        return result

def parse2relations(parse):
    relations = {}
    for p in parse:
        m  = re.search('('+WORD+')\(('+WORD+'-\d+), ('+WORD+'-\d+)\)', p)
        relation = m.group(1)
        head = m.group(2)    
        tail = m.group(3)
        if head not in relations:
            relations[head] = {}
        relations[head][relation] = tail
    return relations

def relation2string(relation,args):
    m = re.search('('+WORD+')-\d+', str(relation))
    func = m.group(1)
    s = func +'('
    for a in args:
        argname = str(a)
        m = re.search('('+WORD+')-\d+', str(args[a]))
        argvalue = m.group(1)
        s+=  argname+'='+argvalue+','
    s += ')'
    return s

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
      

class TopCoderSolver:
    
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

        parser_out = os.popen("~/Downloads/stanford-parser-full-2014-08-27/lexparser.sh "+problem).readlines()

        parse_list = parse2list(parser_out)
        parses = []
        for parse0,parse1 in parse_list: 
            parse0 = re.sub("\s+", " ",parse0)
    #         print(parse0)
            parse_tree = parse2tree(parse0)
#             print(parse_tree)
#             parse_lambda = parse2lambda(parse_tree)
    #         print(len(parse_lambda))
            parse1 = parse1.split('\n') 
            relations = parse2relations(parse1)
#             print(relations)
#             for r in relations:
#                 print(relation2string(r,relations[r]))
            parses.append((parse_tree,relations))
        return parses
        
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
    
    tcs = TopCoderSolver()
    print(tcs.solve('res/return'))
    
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
    
