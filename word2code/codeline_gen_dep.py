'''
Created on May 3, 2015

@author: jordan
'''
import nltk
import re
import copy
from stanford_corenlp import sentence2dependencies
import ast
import os
import problem_parser
from utils import average
import logger


class Node:
    def __init__(self, name = '', parent = None, children = None, ntype = None):
        self.name = name
        self.parent = parent
        self.ntype = ntype
        if not children:
            self.children = []
    
    def deps2tree(self, deps):
        for dep in deps:
            if dep[-2] == dep[-1]: #prevent loop
                continue
            if dep[-2] == self.name:
                node = Node(dep[-1],self)
                if len(dep) > 2:
                    node.ntype = dep[0]
                self.children.append(node)
                node.deps2tree(deps)
        return self

    def tree2deps(self):
        deps = []
        for child in self.children:
            deps.append([child.ntype, self.name, child.name])
            deps.extend(child.tree2deps())
        return deps

    def split_args(self, args):
        level = 0
        s = 0
        args_ = []
        for i,c in enumerate(args):
            if c == '(' or c == '[':
                level += 1
            if c == ')' or c == ']':
                level -= 1
            if level == 0 and c in [',',' ']:
                args_.append(args[s:i])
                s = i+1
        args_.append(args[s:])
        return args_                
    
    def code2tree(self, code):
    #     return(min([mapping(possibility, input_array) for possibility in possibilities]))
    #     ROOT, return
    #     return, min
    #     min, mapping
    #     min, possibility
    #     mapping, possibility
    #     min, possibilities
    #     
    #     each recursive step:
    #         add function to tree
    #         split args
    #         for each arg:
    #             repeat
        print(code)
        m = re.match('\s*(?:(?P<ntype>\w+)=)?(?P<func>\w+)?(?:[\(\[](?P<args>.+)[\)\]])?\s*', code)
        ntype = m.group('ntype')
        print(ntype)
        func = m.group('func')
#         print('func: '+str(func)+' ntype: '+str(ntype))
        if func:
            func_node = Node(func)
            func_node.parent = self
            if ntype:
                func_node.ntype = ntype
            self.children.append(func_node)
        else:
            func_node = self
        args = m.group('args')
        if not args:
            return
        args = func_node.split_args(args)
        for arg in args:
            func_node.code2tree(arg)
        
    def __str__(self):
        s = ''
        if self.ntype:
            s = self.ntype + '='
        s += self.name
        if self.children:
            s += '('
            s += ', '.join([str(child) for child in self.children])
            s += ')'
        return s
        
    def get_nodes(self):
        nodes = []
        nodes.append(self.name)
        for child in self.children:
            nodes.extend(child.get_nodes())
        return nodes
        
        
def dep2word(dep):
    return re.search('(\w+)?-\d+', dep).group(1)

def dep2dict(dep):
    m = re.search('(?P<word>\w+)?-(?P<ind>\d+)', dep)
    return m.groupdict()

# filter dependencies according to words
#     unimportant words should be contracted to their parents
def filter_dep(dependencies, words):
    mappings = {}
#     print(dependencies)
#     print(words)
    new_dependencies = copy.copy(dependencies)
    while True:
        change = False
        for dep in dependencies:
            if dep not in new_dependencies:
                continue
#             child = re.search('(\w+)-\d+', dep[2]).group(1)
            child = dep[2]
#             parent = re.search('(\w+)-\d+', dep[1]).group(1)
            parent = dep[1]
    #         if the child is unimportant add mapping of child to parent
            if dep2word(child) not in words:
#                 print('dep: ' + str(dep))
#                 print('child: ' + str(child))
                mappings[child] = parent
                new_dependencies.remove(dep)
                change = True
    #         if parent is in mapping, do mapping (switch)
            elif parent in mappings:
#                 print('dep: ' + str(dep))
#                 print('parent: ' + str(parent))
#                 print('mapping: ' + str(mappings[parent]))
                new_dependencies.remove(dep)
#                 dep[1] = re.sub('^\w+',mappings[parent],dep[1])
                dep[1] = mappings[parent]
                new_dependencies.append(dep)
                change = True
        if not change:
            break
    return new_dependencies

def clean_dependencies(dependencies):
    clean_deps = []
    for dep in dependencies:
#         print(dep)
#         child = dep2word(dep[2])
        child = dep[2]
#         parent = dep2word(dep[1])
        parent = dep[1]
        clean_deps.append([parent,child])
    return clean_deps


#     calculate distance using dependencies
def get_orig_tree(sentence,translation,codeline):
    sentwords = nltk.word_tokenize(sentence)
    codewords = nltk.word_tokenize(codeline)
    transwords = nltk.word_tokenize(translation)
    transcodedict = dict(zip(transwords,codewords))
#     get dependency tree from sentence
#     print('getting dependencies')
    dependencies = sentence2dependencies(sentence)
    dependencies = [dep for deps in dependencies for dep in deps]
#     print('filtering dependencies')
    dependencies = filter_dep(dependencies, transwords)
#     print('cleaning dependencies')
    dependencies = clean_dependencies(dependencies)
#     transtree = dependencies2tree(dependencies)    
#     calc path distance (length) between any 2 codewords
    return dependencies

#     compare sentence dependencies against code tree
def compare_trees(tree1, tree2):
#         diffs.append(len([dep for dep in orig_tree if [dep2word(dep[1]),dep2word(dep[2])] not in code_tree]))
    return [dep for dep in tree1 if dep not in tree2 and dep[::-1] not in tree2]

def clean_codeline(codeline):
    if ':' in codeline:
        codeline = re.sub('^.+:', '', codeline)
    if '=' in codeline:
        codeline = re.sub('^.+=', '', codeline)
    codeline = re.sub('\sfor\s',', ', codeline)
    codeline = re.sub('\sin\s',', ', codeline)
    codeline = re.sub('\sif\s',', ', codeline)
#     print(codeline)
    return codeline

def check_sentence(sentence, translations, code, n):
    diffs = []
#     print(sentence)
    sentence = sentence.lower()
    for translation,codeline in zip(translations, code):
#         print('getting orig tree')
        logger.logging.debug(sentence.strip())
        translation = clean_codeline(translation)
        orig_tree = get_orig_tree(sentence,translation,codeline)
        logger.logging.debug(orig_tree)
#         print('getting code tree')
        logger.logging.debug(translation.strip())
        root = Node('ROOT')
        root.code2tree(translation)
        code_tree = root.tree2deps()
        logger.logging.debug(code_tree)
#         print('calculating diff')
        diff = compare_trees(orig_tree, code_tree) 
        diffs.append(diff)
        logger.logging.debug(diff)
        logger.logging.debug('-------------------------------------\n')
    return all(len(diff) <= n for diff in diffs)

#     using dependencies to take only most probable translations from codewords to code tree
def likely_possible_trees(sentence,translations,code,k):
    for translation,codeline in zip(translations, code):
#         generate the original tree, this induces path distance between any 2 nodes
        distmat = get_orig_tree(sentence,translation,codeline)
#         generate k minimum spanning trees
        trees = get_min_trees(distmat, k)


def check_sentences(dir,n=0):
    correct = []
    total = 0
    for fname in sorted(os.listdir(dir)):
        with open(os.path.join(dir,fname),'r') as f:
            problem = f.read()
        parse = problem_parser.parse_problem(problem)
        correct_sentences = []
        for sentence_parse in parse['sentences']: 
            sentence = sentence_parse['sentence']
            translations = sentence_parse['translations']
            code = sentence_parse['code']
            if not sentence or not code:
                continue
            correct_sentences.append(check_sentence(sentence, translations, code, n))
        if bool(correct_sentences) and all(correct_sentences):
            correct.append(fname)
        total += bool(correct_sentences)
    print(total)
    print(len(correct))
    print(float(len(correct))/total)
    return correct


if __name__ == '__main__':
#     sentence = 'hello my friend, how are you?'
#     deps = sentence2dependencies(sentence)
#     words = ['hello', 'friend', 'you']
#     print(filter_dep(deps[0], words))

    code = 'return(min([mapping(bla=possibility) for possibility in possibilities]))'
#     parse = ast.parse(code)
#     print(ast.dump(parse,False, True))
#     eval(ast.dump(parse))
    
    root = Node('ROOT')
    root.code2tree(code)
    print(root)
    deps = root.tree2deps()
    print(deps)
    root = Node('ROOT')
    print(root.deps2tree(deps))

#     print(check_sentences('res/text&code3',4))


