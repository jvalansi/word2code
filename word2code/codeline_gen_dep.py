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
from dependency_parser import Node, filter_dep, clean_dependencies




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


