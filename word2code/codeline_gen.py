'''
Created on Apr 26, 2015

@author: jordan
'''
# from utils import *
import logger
import inspect
import re
import copy
import sys
from problem_parser import parse_problem
import os
# from word2codeword import is_func
import string
import nltk
import traceback
from utils import *
import itertools
import operator

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


array = ['input_array', 'possibilities', 'types', 'possibility', 'pair']

non_relevant = []

# #     for all possibilities functions (range,subsets,pairs)
# #         each function space can receive a function or None, without repetition
# #             each variable space can receive a variable or None, with repetition
# def get_possible_codelines(funcs, codeline_vars):
#     codeline_pattern = '{reduce_prefix}{mapping} for possibility in {possibilities} {valid}{reduce_suffix}'
#     tree_pattern = '{func1_prefix}{func2_prefix}{arg1}{comma1}{arg2}{func2_suffix}{comma2}{arg3}{func1_suffix}'

def check_code(code):
    try:
#         print(code)
        eval(code)
    except NameError:
#         print(traceback.print_exc())
        return False
    except TypeError:
#         print(traceback.print_exc())
        return False
    except:
#         print(traceback.print_exc())
        possibility = N
        try:
            eval(code)
        except Exception:
            possibility = range(N)
            return False
#         print(sys.exc_info())
        possibility = range(N)
#         return False
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
    for division in itertools.combinations_with_replacement(range(3), len(funcs)):
        reduces = [func for i, func in enumerate(funcs) if division[i] == 0]
        mappings = [func for i, func in enumerate(funcs) if division[i] == 1]
        filters = [func for i, func in enumerate(funcs) if division[i] == 2]
        mapcodes = all_possible_trees(mappings, array_vars, primitive_vars)
        mapcodes.add('mapping(possibility)')
        filtercodes = all_possible_trees(filters, array_vars, primitive_vars)
        filtercodes.add('valid(possibility)')
        filtercodes.add('')
        reducecodes = set(itertools.permutations(reduces)) if reduces else set([''])
        possibilitiescodes = set(['range(N)', 'subsets(possibility)',
                                  'csubsets(possibility)', 'cpairs(possibility)',
                                  'pairs(possibility)', 'possibilities'])
        for reducecode, mapcode, filtercode, possibilitiescode in itertools.product(reducecodes, mapcodes, filtercodes, possibilitiescodes):
            if reducecode:
                reduceprefix = '('.join(reducecode) + '('
                reducesuffix = ')'*len(reducecode)
            else:
                reduceprefix = ''
                reducesuffix = ''
            if filtercode:
                filtercode = ' if '+filtercode
            possible_code = base_pattern.format(reduceprefix, mapcode, possibilitiescode, filtercode, reducesuffix)
            if check_code(possible_code):
#                 possible_codes.add(possible_code)
                possible_codes.add(possible_code)
            reduceprefix += '['
            reducesuffix = ']'+reducesuffix
            possible_code = base_pattern.format(reduceprefix, mapcode, possibilitiescode, filtercode, reducesuffix)
            if check_code(possible_code):
#                 possible_codes.add(possible_code)
                possible_codes.add(possible_code)
    return possible_codes

def num_of_args(func):
    try:
        argspec = inspect.getargspec(eval(func))
        return len(argspec[0])
    except Exception:
        funcdoc = eval(func).__doc__
#         arg_pattern = r'\w+(?:=\w+)?'
#         possible_args_pattern = r'\[.+\]'
        s = re.search(r'\w+\((\w+(?:=\w+)?(?:,\s)?)*(?:\[.+\])?\)', funcdoc)
        return len(s.groups())

def get_possible_trees(possible_trees, possible_funcs, possible_vars):
    for possible_func in possible_funcs:
        vars_permutation = (itertools.permutations(possible_vars, x) for x in [1, 2])
        vars_permutation = itertools.chain(* vars_permutation)
        for subvars in vars_permutation:
            possible_tree = possible_func+'('+', '.join(subvars)+')'
#     #         print(subtree)
            if not check_code(possible_tree):
                continue
            possible_trees.add(possible_tree)
            possible_vars_ = list(set(possible_vars)-set(subvars))
            possible_vars_.append(possible_tree)
            possible_funcs_ = copy.copy(possible_funcs)
            possible_funcs_.remove(possible_func)
            get_possible_trees(possible_trees, possible_funcs_, possible_vars_)
    return possible_trees

# subtrees = {}

def all_possible_trees(funcs, arrays, primitives):
#     print((possible_funcs, possible_arrays, possible_primitives))
    possible_trees = set()
    for func in funcs:
        funcs_ = copy.copy(funcs)
        funcs_.remove(func)
#TODO: fix usage of subtrees {}, used as global for funcs, but should be used in relation to vars
#         if tuple(possible_funcs_) not in subtrees:
#             subtrees[tuple(possible_funcs_)] = all_possible_trees(possible_funcs_, possible_arrays, possible_primitives)
        subtrees = all_possible_trees(funcs_, arrays, primitives)
#         for subtree in subtrees[tuple(possible_funcs_)]:
        for subtree in subtrees:
            possible_tree = 'all(map(' + func + ', ' + subtree + '))'
            if check_code(possible_tree):
                possible_trees.add(possible_tree)
            possible_tree = func+'('+subtree+')'
            if check_code(possible_tree):
                possible_trees.add(possible_tree)
            possible_tree = func+'(* '+subtree+')'
            if check_code(possible_tree):
                possible_trees.add(possible_tree)
        for split in itertools.product(range(2), repeat=len(funcs_)):
            funcs1 = [func_ for i, func_ in enumerate(funcs_) if split[i] == 0]
            funcs2 = [func_ for i, func_ in enumerate(funcs_) if split[i] == 1]
#             possibilitiescodes = set(['range(N)', 'subsets(possibility)', 'csubsets(possibility)', 'cpairs(possibility)', 'pairs(possibility)', 'possibilities'])
#TODO: fix usage of subtrees {}, used as global for funcs, but should be used in relation to vars
#             if tuple(possible_funcs1) not in subtrees:
#                 subtrees[tuple(possible_funcs1)] = all_possible_trees(possible_funcs1, possible_arrays, possible_primitives)
            subtrees1 = all_possible_trees(funcs1, arrays, primitives)
#             if tuple(possible_funcs2) not in subtrees:
#                 subtrees[tuple(possible_funcs2)] = all_possible_trees(possible_funcs2, possible_arrays, possible_primitives)
            subtrees2 = all_possible_trees(funcs2, arrays, primitives)
#             for subtree1,subtree2 in product(subtrees[tuple(possible_funcs1)],subtrees[tuple(possible_funcs2)]):
            for subtree1, subtree2 in itertools.product(subtrees1, subtrees2):
                possible_tree = func+'('+subtree1+', '+subtree2+')'
                if check_code(possible_tree):
                    possible_trees.add(possible_tree)
#         for split in product(range(3), repeat=len(funcs_)):
#             funcs1 = [func_ for i, func_ in enumerate(funcs_) if split[i] == 0]
#             funcs2 = [func_ for i, func_ in enumerate(funcs_) if split[i] == 1]
#             funcs3 = [func_ for i, func_ in enumerate(funcs_) if split[i] == 2]
#             if tuple(funcs1) not in subtrees:
#                 subtrees[tuple(funcs1)] = all_possible_trees(funcs1, arrays, primitives)
#             if tuple(funcs2) not in subtrees:
#                 subtrees[tuple(funcs2)] = all_possible_trees(funcs2, arrays, primitives)
#             if tuple(funcs3) not in subtrees:
#                 subtrees[tuple(funcs3)] = all_possible_trees(funcs3, arrays, primitives)
#             for subtree1, subtree2, subtree3 in product(subtrees[tuple(funcs1)], subtrees[tuple(funcs2)], subtrees[tuple(funcs3)]):
#                 for possibilitiescode in possibilitiescodes:
#                     possible_tree = func+'('+'[{} for possibility in {} if {}]'.format(subtree1, possibilitiescode, subtree2)+')'
#                     if check_code(possible_tree):
#                         possible_trees.add(possible_tree)
    for array_ in arrays:
        possible_trees.add(array_)
        for primitive in primitives:
#             print(array)
#             print(primitive)
            possible_tree = array_+'['+primitive+']'
            if check_code(possible_tree):
                possible_trees.add(possible_tree)
    for primitive in primitives:
        possible_trees.add(primitive)
#     print(possible_trees)
    return possible_trees
#     foreach node:
#     add primitives
#     add arrays
#     foreach array: foreach primitive: add array[primitives]
#     foreach func:
#         all_trees = all_possible_trees(nodes - func)
#         if 1 arg: for tree in trees: add func(tree)
#         if 2 args: for (tree1, tree2) in permutation(trees,2): add func(tree1, tree2)



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
#     functions = [word2codewords(word, n) for (p, isfunc, word) in funcwords]
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
        isfunc = codeword in ['return', 'mapping', 'valid']
        isfunc |= hasattr(eval(codeword), '__call__')
    except Exception:
        isfunc = False
    return isfunc


def check_translation(sentence, translation, codeline):
#     print(sentence)
#     print(codeline)
#     print(translation)
    sentwords = nltk.word_tokenize(sentence)
#     print(sentwords)
    codewords = nltk.word_tokenize(codeline)
    transwords = nltk.word_tokenize(translation)
    transcodedict = dict(zip(transwords, codewords))
    full_transwords = []
    for transword in transwords:
        full_transwords.extend(transword.split('_'))
    if 'return' in codewords:
        return True
    if codewords[0] == 'possibilities':
        return True
    if ':' in full_transwords:
        idx = operator.indexOf(full_transwords, ':')
        full_transwords = full_transwords[idx+1:]
    if '=' in full_transwords:
        idx = operator.indexOf(full_transwords, '=')
        full_transwords = full_transwords[idx+1:]
    relevantwords = [transword for transword in transwords if transword in sentwords]
#     print(relevantwords)
    otherwords = set(full_transwords) - set(sentwords)
    otherwords -= set(['(', ')', 'for', 'in', '[', ']', 'if', ',',
                       'possibility', 'possibilities', 'valid', '0',
                       '1', '2', '*', 'n', 'range', 'len', '=', 'subsets',
                       'and', 'int', 'valid1', 'sum', 'mapping'])
#         sentence_otherwords.extend(otherwords)
    non_relevant.extend(otherwords)
#         if otherwords:
#             print('other words')
#             print(otherwords)
#             return False
#     print(relevantwords)
    relevantcode = [transcodedict[word] for word in relevantwords]
    funcs = [word for word in relevantcode if is_func(word) and word != 'return']
#     possible_vars = [word for word in relevantcode if not is_func(word)]
    possible_vars = set(vars) - set(list(string.punctuation)+['\'\'','``'])
    possible_vars -= set(['for', 'in', 'if', 'else'])
    possible_vars = list(possible_vars)
    array_vars = [var for var in possible_vars if var in array]
    if 'possibility' not in array_vars: array_vars.append('possibility')
    primitive_vars = [var for var in possible_vars if var not in array]
    if '0' not in primitive_vars: primitive_vars.append('0')
    if '1' not in primitive_vars: primitive_vars.append('1')
    if "'0'" not in primitive_vars: primitive_vars.append("'0'")
    if "'1'" not in primitive_vars: primitive_vars.append("'1'")
    if len(funcs) > 4:
        logger.logging.info('too many')
        logger.logging.info(funcs)
        logger.logging.info(array_vars)
        logger.logging.info(primitive_vars)
        logger.logging.info(codeline)
        return False
    codeline = re.sub(r'.+:\s+', '', codeline.strip())
    codeline = re.sub(r'.+=\s+', '', codeline.strip())
    codeline = re.sub(r'return\s*\((.+)\)', '\\1', codeline)
    if codeline not in all_possible_trees(funcs, array_vars, primitive_vars):
        logger.logging.info('not found')
        logger.logging.info(funcs)
        logger.logging.info(array_vars)
        logger.logging.info(primitive_vars)
        logger.logging.info(codeline)
        return False
    return True

# def check_codewords(codewords, transwords, sentwords,n):
#     transcodedict = dict(zip(transwords, codewords))
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
def check_sentence(sentence, translations, code, n=0):
    sentwords = nltk.word_tokenize(sentence.lower())
#     N = len(sentwords)
    sentence_otherwords = []
    for translation, codeline in zip(translations, code):
        if not codeline:
            continue
        if not check_translation(sentence, translation, codeline):
#         if not check_codewords(codewords, transwords, sentwords, n):
            return False
#     print(sentence_otherwords)
    non_relevant.extend(sentence_otherwords)
#     if not sentence_otherwords:
#         print(sentence)
#     print('Success')
    return True
#     return not(sentence_otherwords)

def check_problem(problem_dir, fname, n=0):
    with open(os.path.join(problem_dir, fname), 'r') as f:
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
    return correct_sentences

def check_sentences(sentences_dir, n=0):
    correct = []
    total = 0
    for fname in sorted(os.listdir(sentences_dir)):
        correct_sentences = check_problem(sentences_dir, fname, n)
        if bool(correct_sentences) and all(correct_sentences):
            correct.append(fname)
        total += bool(correct_sentences)
    print(total)
    print(float(len(correct))/total)
    return correct


if __name__ == '__main__':
    FUNCS = ['percentage']
    ARRAY_VARS = ['possibility']
    PRIMITIVE_VARS = ["'1'", '0', '1']
    POSSIBLE_CODE = all_possible_trees(FUNCS,
                                        ARRAY_VARS,
                                        PRIMITIVE_VARS)
    print(len(POSSIBLE_CODE))
    with open('res/possible_code', 'w') as fmain:
        fmain.write('\n'.join(POSSIBLE_CODE))

#     print(countOf(possibility0, types[0]))

    PROBLEM_DIR = 'res/text&code5'
#     print(check_sentences(dir))

    FNAME = 'CompetitionStatistics.py'
    FNAME = 'Elections.py'
    print(check_problem(PROBLEM_DIR, FNAME))
