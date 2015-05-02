'''
Created on Apr 26, 2015

@author: jordan
'''
from utils import *
import inspect
import re
import copy
import sys
from problem_parser import parse_problem
import os
# from word2codeword import is_func
import string
import logger
import nltk

N = 2
input_array = range(N)
input_array0 = range(N)
input_array1 = range(N)
input_array2 = range(N)
types = range(N)
input_int = N
input_int0 = N
input_int1 = N
input_int2 = N
possibilities = list(subsets(input_array))
possibility = range(N)
possibility0 = range(N)
possibility1 = range(N)
possibility2 = range(N)
mapping = lambda possibility: N
mapping0 = lambda possibility: N
mapping1 = lambda possibility: N
mapping2 = lambda possibility: N
valid = lambda possibility: True 
valid0 = lambda possibility: True 
valid1 = lambda possibility: True 
valid2 = lambda possibility: True 
element = N


array = ['input_array','possibilities','types','possibility','pair']

non_relevant = []

#     for all possibilities functions (range,subsets,pairs)
#         each function space can receive a function or None, without repetition
#             each variable space can receive a variable or None, with repetition
def get_possible_codelines(funcs, vars):
    codeline_pattern = '{reduce_prefix}{mapping} for possibility in {possibilities} {valid}{reduce_suffix}'
    tree_pattern = '{func1_prefix}{func2_prefix}{arg1}{comma1}{arg2}{func2_suffix}{comma2}{arg3}{func1_suffix}'
    
    
def check_code(code):
    try:
#         print(code)
        eval(code)
    except NameError:
#         print(sys.exc_info())
        return False
    except:
#         print(sys.exc_info())
        return False
    return True
    
    
def get_possible_code(funcs, array_vars, primitive_vars):
    if 'possibility' not in array_vars: array_vars.append('possibility')
    if 'possibilities' in array_vars: array_vars.remove('possibilities')
#     vars.append('types[0]')
#     possible_codes = all_possible_trees(set(), funcs, vars)
    possible_codes = all_possible_trees(funcs, array_vars, primitive_vars)
    if 'mapping' in funcs: funcs.remove('mapping')
    if 'valid' in funcs: funcs.remove('valid')
    if 'subsets' in funcs: funcs.remove('subsets')
    if 'csubsets' in funcs: funcs.remove('csubsets')
    if 'range' in funcs: funcs.remove('range')
    base_pattern = '{}{} for possibility in {}{}{}'
    for division in combinations_with_replacement(range(3), len(funcs)):
        reduces = [func for i,func in enumerate(funcs) if division[i] == 0]
        mappings = [func for i,func in enumerate(funcs) if division[i] == 1]
        filters = [func for i,func in enumerate(funcs) if division[i] == 2]
        mapcodes = all_possible_trees(mappings, array_vars, primitive_vars)
        mapcodes.append('mapping(possibility)')
        filtercodes = all_possible_trees(filters, array_vars, primitive_vars)
        filtercodes.append('valid(possibility)')
        filtercodes.append('')        
        reducecodes = set(permutations(reduces)) if reduces else set([''])
        possibilitiescodes = set(['range(N)', 'subsets(possibility)', 'csubsets(possibility)', 'cpairs(possibility)', 'pairs(possibility)', 'possibilities'])
        for reducecode,mapcode,filtercode,possibilitiescode in product(reducecodes,mapcodes,filtercodes,possibilitiescodes):
            if reducecode:
                reduceprefix = '('.join(reducecode) + '('
                reducesuffix = ')'*len(reducecode)
            else:
                reduceprefix = ''
                reducesuffix = ''
            if filtercode:
                filtercode = ' if '+filtercode
            possible_code = base_pattern.format(reduceprefix,mapcode,possibilitiescode,filtercode,reducesuffix)             
            if check_code(possible_code):
#                 possible_codes.add(possible_code)
                possible_codes.append(possible_code)
            reduceprefix += '['
            reducesuffix = ']'+reducesuffix
            possible_code = base_pattern.format(reduceprefix,mapcode,possibilitiescode,filtercode,reducesuffix)             
            if check_code(possible_code):
#                 possible_codes.add(possible_code)
                possible_codes.append(possible_code)
            
    return possible_codes

def num_of_args(func):
    try:
        argspec = inspect.getargspec(eval(func))
        return len(argspec[0])
    except:
        funcdoc = eval(func).__doc__
        arg_pattern = '\w+(?:=\w+)?'
        possible_args_pattern = '\[.+\]'
        s = re.search('\w+\((\w+(?:=\w+)?(?:,\s)?)*(?:\[.+\])?\)', funcdoc)
        return len(s.groups())
        

def get_possible_trees(possible_trees, funcs, vars):
    for func in funcs:
        for subvars in chain(*map(lambda x: permutations(vars, x), [1,2])):
            possible_tree = func+'('+', '.join(subvars)+')'         
#     #         print(subtree)       
            if not check_code(possible_tree):
                continue
            possible_trees.add(possible_tree)
            vars_ = list(set(vars)-set(subvars))
            vars_.append(possible_tree)
            funcs_ = copy.copy(funcs)
            funcs_.remove(func)
            get_possible_trees(possible_trees, funcs_, vars_)
    return possible_trees
    
def all_possible_trees(funcs, arrays,primitives):
    possible_trees = []
    for func in funcs:
        funcs_ = copy.copy(funcs)
        funcs_.remove(func)
        subtrees = all_possible_trees(funcs_, arrays, primitives)
        for subtree in subtrees:
            possible_tree = func+'('+subtree+')' 
            if check_code(possible_tree):
                possible_trees.append(possible_tree)
        for subtree1,subtree2 in permutations(subtrees,2):
            possible_tree = func+'('+subtree1+', '+subtree2+')'
            if check_code(possible_tree):
                possible_trees.append(possible_tree)
    for array in arrays:
        possible_trees.append(array)
        for primitive in primitives:
            possible_tree = array+'['+primitive+']' 
            if check_code(possible_tree):
                possible_trees.append(possible_tree)
        possible_trees.append(array+'[0]')
    for primitive in primitives:
        possible_trees.append(primitive)
    return possible_trees
#     foreach node:
#     add primitives
#     add arrays
#     foreach array: foreach primitive: add array[primitives]
#     foreach func:
#         all_trees = all_possible_trees(nodes - func)
#         if 1 arg: for tree in trees: add func(tree)
#         if 2 args: for (tree1,tree2) in permutation(trees,2): add func(tree1,tree2)



# #     input: sentence
# #     output: code
# #     process:
# #         get probable function words from sentence
# #         get probable functions from words
# #         get primitives from sentence
# #         try all combinations
# #             add castings and for loops whenever needed or possible
# #         
# def sentence2code(sentence, n, codewords):
#     funcwords = get_label_probs(sentence, 'mapping')[:n]
#     functions = [word2codewords(word,n) for (p, isfunc, word) in funcwords]
#     primitives = list(set([line['word'] for line in sentence]) & set(primitive))
#     for functions_option in product(*functions):
#         codewords_option = functions_option + ['(',')']*len(functions_option) + primitives + array
#         if codewords in codewords_option:
#             return True
#     return False
# 
# #     input: sentence
# #     output: most likely code words
# def sentence2codewords(sentence):
#     codewords = []
#     for word in nltk.word_tokenize(sentence):
#         likelihoods = word2codewords(word)
#         codewords.append(likelihoods)
#     return codewords

def is_func(codeword):         
    try:
        isfunc = codeword in ['return','mapping','valid'] or hasattr(eval(codeword), '__call__')
    except:
        isfunc = False
    return isfunc


def check_translation(codeline,codewords,transwords,sentwords):
    transcodedict = dict(zip(transwords,codewords))
    full_transwords = []
    for transword in transwords:
        full_transwords.extend(transword.split('_')) 
    if ':' in full_transwords:
        full_transwords = full_transwords[indexOf(full_transwords, ':')+1:]
    if '=' in full_transwords:
        full_transwords = full_transwords[indexOf(full_transwords, '=')+1:]
    relevantwords = [transword for transword in transwords if transword in sentwords]
#         print(relevantwords)
    otherwords = set(full_transwords) - set(sentwords) - set(['(', ')', 'for', 'in', '[', ']', 'if', ',', 'possibility', 'possibilities', 'valid', '0', '1', '2', '*', 'n', 'range', 'len', '=', 'subsets', 'and', 'int', 'valid1', 'sum', 'mapping']) 
#         sentence_otherwords.extend(otherwords)
    non_relevant.extend(otherwords)
#         if otherwords:
#             print('other words')
#             print(otherwords)
#             return False
    relevantcode = [transcodedict[word] for word in relevantwords]
    funcs = [word for word in relevantcode if is_func(word) and word != 'return']
    vars = [word for word in relevantcode if not is_func(word)]
    vars = list(set(vars) - set(list(string.punctuation)+['\'\'','``']) - set(['for','in','if','else']))
    array_vars = [var for var in vars if var in array]
    primitive_vars = [var for var in vars if var not in array]
    if len(funcs) > 4:
        logger.logging.info('too many')
        logger.logging.info(funcs)
        logger.logging.info(array_vars)
        logger.logging.info(primitive_vars)
        logger.logging.info(codeline) 
        return False
    codeline = re.sub('.+:\s+','',codeline.strip())
    codeline = re.sub('return\s*\((.+)\)','\\1',codeline) 
    if codeline not in get_possible_code(funcs, array_vars, primitive_vars):
        logger.logging.info('not found')
        logger.logging.info(funcs)
        logger.logging.info(array_vars)
        logger.logging.info(primitive_vars)
        logger.logging.info(codeline) 
        return False
    return True
 
# def check_codewords(codewords,transwords,sentwords,n):
#     transcodedict = dict(zip(transwords,codewords))
#     full_transwords = []
#     for transword in transwords:
#         full_transwords.extend(transword.split('_')) 
#     relevantwords = [transword for transword in transwords if transword in sentwords]
#     otherwords = set(full_transwords) - set(sentwords)
# #      - set(['(', ')', 'for', 'in', '[', ']', 'if', ',', 'possibility', 'possibilities', 'valid', '0', '1', '2', '*', 'n', 'range', 'len', '=', 'subsets', 'and', 'int', 'valid1', 'sum', 'mapping']) 
# #     non_relevant.extend(otherwords)
#     for otherword in otherwords:
#         if otherword not in transcodedict:
#             continue
#         non_relevant.append(transcodedict[otherword])
#     relevantwords = [clean_word(word) for word in relevantwords]
#     for relevantword in relevantwords:
#         if not relevantword:
#             continue
#         codeword = transcodedict[relevantword]
#         if not is_func(codeword):
#             continue 
#         likelycodewords = word2codewords(relevantword)
#         issimilar = codeword in zip(*likelycodewords)[1][:n]
#         if not issimilar:
#             print(relevantword)
#             print(codeword_dict[codeword])
#             print(likelycodewords)
#             return False
#     return True
 
          
#     input: sentence, translations, code
#     output: 
#         are all relevant words similar to code
#         are all other words arrays or primitives
def check_sentence(sentence,translations, code,n=0):
    sentwords = nltk.word_tokenize(sentence.lower())
    N = len(sentwords)
    sentence_otherwords = []
    for translation,codeline in zip(translations,code):
        codewords = nltk.word_tokenize(codeline)
        transwords = nltk.word_tokenize(translation)
        if not codewords:
            continue
        if not check_translation(codeline, codewords, transwords, sentwords):
#         if not check_codewords(codewords, transwords, sentwords, n):
            return False
#     print(sentence_otherwords)
    non_relevant.extend(sentence_otherwords)
#     if not sentence_otherwords:
#         print(sentence)
#     print('Success')
    return True
#     return not(sentence_otherwords)
          
def check_sentences(dir,n=0):
    correct = []
    total = 0
    for fname in sorted(os.listdir(dir)):
        with open(os.path.join(dir,fname),'r') as f:
            problem = f.read()
        parse = parse_problem(problem)
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
    print(float(len(correct))/total)
    return correct


if __name__ == '__main__':
    funcs = ['eq', 'countOf', 'countOf']
    array_vars = ['types', 'possibility']
    primitive_vars = ['possibility1', 'possibility0']
    possible_code = get_possible_code(funcs, array_vars,primitive_vars)
    print(len(possible_code))
    with open('res/possible_code','w') as f:
        f.write('\n'.join(possible_code))

#     print(countOf(possibility0, types[0]))
    
#     print(check_sentences('res/text&code3'))
