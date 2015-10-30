'''
Created on May 3, 2015

@author: jordan
'''
import nltk
import re
# from stanford_corenlp import sentence2dependencies
import os
import problem_parser
import logger
from dependency_parser import Node, filter_dep, clean_dependencies,\
    sentence2dependencies, dep2word, clean_duplicates
import astor
import ast
from utils import clean_codeline, get_codeline_type, is_func, get_transdict,\
    get_sentence_type, add_codeline_prefix
from collections import Counter
import collections
from stanford_corenlp import tokenize_sentences
            
#     problem:
#         codeline: eq(len(diff(input_array, possibility)), 1)
#         dependencies: eq(diff(input_array, possibility), 1) 
            
def gen_codelines(funcs, variables, deps):
    '''
    generate codeline from sentence
    >>> funcs = ['eq', 'diff']
    >>> variables = ['input_array', 'possibility', 1]
    >>> deps = 
    >>> 'eq(len(diff(input_array, possibility)), 1)' in gen_codelines(funcs, variables)
    True
    
    :param funcs:
    :param variables:
    '''


def get_root(deps, rootword):
    sentwords = [word for dep in deps for word in dep[-2:]]
    rootwords = [word for word in sentwords if rootword == dep2word(word) ]
    if not rootwords:
        return
    root = Node(rootwords[0])
    return root

def get_expected_codeline_gen(code, words=None):
    tree = get_code_tree(code, words) 
    codeline = str(tree)
    return codeline

def get_possible_codelines(sentence, transdict, sentence_type=None, codeline_type=None):
    trees = get_all_sent_trees(sentence, transdict, sentence_type, codeline_type) 
    codelines = map(str, trees)
    return codelines

def get_all_sent_trees(sentence, transdict, sentence_type=None, codeline_type=None):
    trees = []
    for transword,codeword in transdict.items():
        if not is_func(codeword):
            continue
        root = get_sent_tree(sentence, transdict, transword)
        trees.append(root)
    if codeline_type == 'possibilities':
        if sentence_type == 'return': 
            trees.append(Node(code='subsets(input_array)'))
            trees.append(Node(code='csubsets(input_array)'))
            trees.append(Node(code='transformations(input_array)'))
            trees.append(Node(code='range(inf)'))
        else:
            trees.append(Node(code='pairs(possibility)'))
            trees.append(Node(code='cpairs(possibility)'))
        trees.append(Node(code='range(N)'))
    return trees

def get_sent_tree(sentence, transdict, rootname):
    deps = sentence2dependencies(sentence)[0] #TODO: fix
    logger.logging.debug(rootname)
    root = get_root(deps, rootname)
    if not root:
        logger.logging.debug('no root')
        root = Node('possibility')
        return root
    root.deps2tree(deps)
    logger.logging.debug(root)
    root.clean_ind()
    words = transdict.keys()
    root.filter_words(words)
    logger.logging.debug(root)
    root.clear_ntypes()
    root.translate(transdict)
    logger.logging.debug(root)
#     root.rearrange()
    root = clean_duplicates(root)
    root.fix_type()
    logger.logging.debug(root)
    return root

def get_code_tree(code, words=None):
    root = Node()
    root.code2tree(code)
    if words != None:
        root.filter_words(words)
    return root

missing_words = []

def check_sentence(sentence_parse, n):
    diffs = []
    sentence = sentence_parse['sentence'].strip()
    translations = sentence_parse['translations']
    code = sentence_parse['code']
    method = sentence_parse['method']
    sentence_type = get_sentence_type(sentence, translations, code, method)
    sentwords = sentwords = tokenize_sentences(sentence)[0]
    results = []
    for translation,codeline in zip(translations, code):
        logger.logging.debug(codeline)
        codeline_type = get_codeline_type(codeline)
        if codeline_type in ['', 'return']:
            continue
        codeline = clean_codeline(codeline)
        translation = clean_codeline(translation)
        transdict = get_transdict(translation, codeline)
        codedict = get_transdict(codeline, translation)
        transwords = transdict.keys()
        codewords = codedict.keys()
#         codewords = [codeword for codeword in codewords if codedict[codeword] in sentwords]
        logger.logging.debug(codewords)
        code_tree = get_code_tree(codeline, codewords)
        if not code_tree or not code_tree.name:
            logger.logging.debug(sentence)
            continue
        sent_trees = get_all_sent_trees(sentence, transdict, sentence_type, codeline_type)
        codeline_results = []
        for sent_tree in sent_trees:
            diff = code_tree.compare(sent_tree)
            codeline_results.append(len(diff))
        if codeline_results and min(codeline_results) > n:
            sent_tree = sent_trees[codeline_results.index(min(codeline_results))]
            logger.logging.info(sentence)
            logger.logging.info(code_tree)
            logger.logging.info(sent_tree)
            diff = code_tree.compare(sent_tree)
            logger.logging.info(diff)
            missing_words.extend([word for dep in diff for word in dep[-2:]])
            results.append(False)
        else:
            results.append(True)
    return all(results)

#     using dependencies to take only most probable translations from codewords to code tree
def likely_possible_trees(sentence,translations,code,k):
    for translation,codeline in zip(translations, code):
#         generate the original tree, this induces path distance between any 2 nodes
        distmat = get_orig_tree(sentence,translation,codeline)
#         generate k minimum spanning trees
        trees = get_min_trees(distmat, k)


def check_problem(path, fname, n=0):
    with open(os.path.join(path, fname),'r') as f:
        problem = f.read()
    parse = problem_parser.parse_problem(problem)
    correct_sentences = []
    for sentence_parse in parse['sentences']: 
        sentence = sentence_parse['sentence']
        code = sentence_parse['code']
        if not sentence or not code:
            continue
        correct_sentences.append(check_sentence(sentence_parse, n))
    if bool(correct_sentences) and all(correct_sentences):
        return True
    return False

def check_problems(path, n=0, success=True):
    correct = []
    fail = []
    total = 0
    for fname in sorted(os.listdir(path)):
        if not fname.endswith('.py'):
            continue
        logger.logging.info(fname)
        result = check_problem(path, fname, n)
        if result:
            correct.append(fname)
        else:
            fail.append(fname)
        total += 1
    print(total)
    results = correct if success else fail
    print(len(results))
    print(float(len(results))/total)
    return results
        

def main():
    logger.console.setLevel(logger.logging.DEBUG)
    problems_path = 'res/text&code8'
    print(check_problems(problems_path, success=True))
    fname = 'CandidatesSelectionEasy.py'
    print(check_problem(problems_path, fname))
    print(Counter(missing_words))
    
#     success:    
# ['AlienAndPassword.py', 'AverageAverage.py', 'BlockTower.py', 'ChocolateBar.py',
#  'ChristmasTreeDecorationDiv2.py', 'CucumberMarket.py', 'Elections.py', 'FoxAndG
# ame.py', 'MountainRanges.py', 'SumOfPower.py', 'TournamentsAmbiguityNumber.py', 
# 'WinterAndMandarins.py']
    
if __name__ == '__main__':
    main()

    