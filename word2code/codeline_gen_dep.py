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
    sentence2dependencies, dep2word
import astor
import ast
from utils import clean_codeline, get_codeline_type, is_func, get_transdict
from collections import Counter
import collections
            
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

def get_sent_tree(sentence, transdict, words, rootname):
    deps = sentence2dependencies(sentence)[0] #TODO: fix
    root = get_root(deps, rootname)
    if not root:
        return
    root.deps2tree(deps)
    root.clean_ind()
    root.filter_words(words)
    root.clear_ntypes()
    root.translate(transdict)
    root.rearrange()
    root.fix_type()
    return root

def get_code_tree(code, words):
    try:
        parse = ast.parse(code.strip())
    except Exception:
        logger.logging.warning('could\'nt parse')
        return
    if not parse.body:
        return
    if not hasattr(parse.body[0], 'value'):
        logger.logging.warning('no value node')
        return
    root = Node()
    root.ast2tree(parse.body[0].value)
    root.filter_words(words)
    return root

missing_words = []

def check_sentence(sentence, translations, code, n):
    diffs = []
    sentence = sentence.strip()
    sentwords = nltk.word_tokenize(sentence)
    for translation,codeline in zip(translations, code):
        logger.logging.debug(codeline)
        codeline_type = get_codeline_type(codeline)
        if codeline_type == 'return':
            continue
        codeline = clean_codeline(codeline)
        translation = clean_codeline(translation)
        transdict = get_transdict(translation, codeline)
        transwords = transdict.keys()
        words = [word for word in transwords if word in sentwords]
        missing_in_translation = [word for word in transwords if word not in sentwords] 
        missing_words.extend(missing_in_translation)
        words = transwords
        code_tree = get_code_tree(translation, words)
        if not code_tree:
            continue
        rootword = code_tree.name
        code_tree.translate(transdict)
        sent_tree = get_sent_tree(sentence, transdict, words, rootword)
        if not sent_tree:
            continue
        diff = code_tree.compare(sent_tree)
        if len(diff) > n: 
            logger.logging.info(sentence)
            logger.logging.info(code_tree)
            logger.logging.info(sent_tree)
            logger.logging.info(diff)
            return False
    return True

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
        translations = sentence_parse['translations']
        code = sentence_parse['code']
        if not sentence or not code:
            continue
        correct_sentences.append(check_sentence(sentence, translations, code, n))
    if bool(correct_sentences) and all(correct_sentences):
        return True
    return False

def check_problems(path, n=0):
    correct = []
    total = 0
    for fname in sorted(os.listdir(path)):
        if not fname.endswith('.py'):
            continue
        print(fname)
        result = check_problem(path, fname, n)
        if result:
            correct.append(fname)
        total += 1
    print(total)
    print(len(correct))
    print(float(len(correct))/total)
    return correct

def main():
    problems_path = 'res/text&code8'
    print(check_problems(problems_path))
    fname = 'AlienAndPassword.py'
#     fname = 'BasketsWithApples.py'
    fname = 'BlockTower.py'
#     fname = 'TextStatistics.py'
#     print(check_problem(problems_path, fname))
    print(Counter(missing_words))

    
if __name__ == '__main__':
    main()

    