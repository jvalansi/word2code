'''
Created on Apr 28, 2015

@author: jordan
'''
import os
import problem2sentence
import sentence2word
import word2codeword
import codeline_gen
import json
from problem2sentence import get_sentences_probabilities
from sentence2word import get_label_probs
from word2codeword import count_translations, is_func, word2codewords
from problem_parser import parse_problem, compose_problem
import copy
from itertools import product, combinations
from codeline_gen import all_possible_trees
from utils import *
import numpy

def get_sentence_type(sentences_json, sentence, n):
    sentind = sentences_json.index(sentence)
    for sentence_type in problem2sentence.types:
        sentprobs = get_sentences_probabilities(sentences_json, sentence_type)
        sentprobs = sorted(sentprobs, reverse=True)
        sentinds = [i for (sentprob, i, important) in sentprobs[:n]]
        if sentind in sentinds:
            return sentence_type


def get_important_sentences(problem_json, n, symbol):
    sentprobs = get_sentences_probabilities(problem_json, symbol)
    sentprobs = sorted(sentprobs, reverse=True)
    if not all([not important for (sentprob, i, important) in sentprobs[n:]]):
        return []
    return([i for (sentprob, i, important) in sentprobs[:n]])

# for each sentence:
#     get sentence type
#     for each codeline type:
#         get probable words
#         get probable codewords
#         generate possible codelines
#     generate possible code

#    generate code:
#        for all sentence type combinations ((n+1)^types)
#              for all possible word types (m):
#                 for all codeword combinations ((1/p)^m)
#                     for all possible codelines

# def check_problem(fname, sentence_dir, n):
# #     get all important sentences
#     sentences = get_important_sentences(fname, sentence_dir, n)
# #     for each sentence get all important words
#     for sentence in sentences:
#         words = get_important_words(fname, word_dir, m, sentence)
# #         for each word get all probable codewords
#         for word in words:
#             codewords = get_likely_codewords(word)
# #         for each codewords combination get all possible codelines
#         for codeword_combination in
#
# #     generate all possible code
#     gen_code()
# #         check if solves
#
# def gen_code():
#

def get_important_words(sentence, sentence_type):
    sentprobs = get_label_probs(sentence, sentence_type)
    return([word for (sentprob, important, word) in sentprobs[:m]])

def get_likely_codewords(word, translations_count, p_thresh):
    codewords = word2codewords(word, translations_count, p_thresh)
    if not codewords:
        return False
    codewords = [(p, c) for p, c in codewords if p >= p_thresh]
    codewords = [(p, c) for p, c in codewords if is_func(c)]
    codewords = [(p, c) for p, c in codewords if c not in possibilities_funcs]        
    return(codewords)

def get_possible_codelines(codewords, word_type):
    funcs = [word for word in codewords if is_func(word) and word != 'return']
    variables = [word for word in codewords if not is_func(word)]
    array_vars = [var for var in variables if isinstance(var, basestring)]
    if 'possibility' not in array_vars: array_vars.append('possibility')
    primitive_vars = [var for var in variables if not isinstance(var, basestring)]
    possible_codelines = all_possible_trees(funcs, array_vars, primitive_vars)
    new_possible_codelines = set()
    for possible_codeline in possible_codelines:
        possible_codeline = word_type +' = lambda possibility: ' + possible_codeline
        new_possible_codelines.add(possible_codeline)
    return(new_possible_codelines)

def get_type_codelines(word_type, type_codewords):
    type_codelines = set()
    type_codelines.add((1.0, word_type +' = lambda possibility: possibility'))
    for codeword_product in product(*type_codewords):
        for codeword_combination in combinations(codeword_product, 2):
            probs, codewords = zip(*codeword_combination) 
            p = numpy.prod(probs)
            possible_codelines = get_possible_codelines(codewords, 
                                                        word_type)
            possible_codelines = [(p, type_codeline) for type_codeline in possible_codelines]
            type_codelines.update(possible_codelines)
    type_codelines = sorted(type_codelines, reverse=True)[:100]
    return type_codelines

def get_type_codewords(important_words, translations_count, p_thresh):
    type_codewords = []
    for word in important_words:
        likely_codewords = get_likely_codewords(word,
                                                translations_count,
                                                p_thresh)
        if not likely_codewords:
            continue
        type_codewords.append(likely_codewords)
    return type_codewords

possibilities_funcs = ['pairs', 'cpairs', 'subsets', 'csubsets'] 

def generate_possible_code(word_json, translations_count, p_thresh, sentence_parse):
#     print('generate_possible_code')
    possible_codes = []
    possibilities_codelines = set()
    for func in possibilities_funcs:
        possibile_codelines =  get_possible_codelines([func], 'possibilities')
        possibile_codelines = [(1.0, codeline) for codeline in possibile_codelines]
        possibilities_codelines.update(possibile_codelines)
#     print('possibilities_codelines')
    print(len(possibilities_codelines))
    possible_codes.append(possibilities_codelines)
#     for translation, codeline in zip(sentence_parse['translations'], sentence_parse['code']):
#         codewords = nltk.word_tokenize(codeline)
#         type = codewords[0]
#         if type not in sentence2word.types:
#             continue
#         print('codeline:')
#         print(codeline)
    for word_type in sentence2word.types:
        important_words = get_important_words(word_json, word_type)
        type_codewords = get_type_codewords(important_words, translations_count, p_thresh)
        type_codelines = get_type_codelines(word_type, type_codewords)
        print(len(type_codelines))
#         if codeline.strip() not in type_codelines:
#             print(False)
        possible_codes.append(type_codelines)
    return_codelines = set()
    return_codelines.add((1.0, 'return(reduce(map(mapping, filter(valid, possibilities(input_array)))))'))
    possible_codes.append(return_codelines)
    product_code = []
    for possible_code in product(*possible_codes):
        probs, codes = zip(*possible_code)
        p = numpy.prod(probs)
        product_code.append((p, codes))
    product_code = sorted(product_code, reverse=True)[:100]
    product_code = [code for p, code in product_code]
#     print(len(list(product(* possible_code))))
    return product_code

def check_solution(solution, fname):
    with open('temp.py', 'w') as f:
        f.write(compose_problem(solution))
    if os.path.exists('temp.pyc'):
        os.remove('temp.pyc')
    import temp
    reload(temp)
    try:
        result = temp.example0()
#         print(result)
        if result:
            result = temp.example1()
            if result:
                sol_dir = 'res/solutions/'
                if not os.path.exists(sol_dir):
                    os.mkdir(sol_dir)
                with open(os.path.join(sol_dir, fname), 'w') as f:
                    f.write(compose_problem(solution))
                return True
    except Exception:
#                 traceback.print_exc()
        pass
    return False

def build_return(types):
    inds, types = zip(*types)
    valid0 = 'filter(valid0, ' if 'valid' in types else ''
    valid0_ = ')' if 'valid' in types else ''
    mapping0 = 'map(mapping0, ' if 'mapping' in types else ''
    mapping0_ = ')' if 'mapping' in types else ''
    reduce0 = 'reduce0(' if 'reduce' in types else ''
    reduce0_ = ')' if 'reduce' in types else ''
    base_pattern = 'return({}reduce(map(mapping, filter(valid, {}{} possibilities(input_array))))){}{}{}'
    return base_pattern.format(reduce0, mapping0, valid0, valid0_, mapping0_, reduce0_)

def check_solutions(possible_solutions, parse, possible_types, tries, fname):
    return_statement = build_return(possible_types)
    for j, possible_codes in enumerate(product(* possible_solutions)):
        if not j%1000:
            print(j)
        if j > tries:
            return False
        new_parse = copy.deepcopy(parse)
        success = False
        for i, possible_code in enumerate(possible_codes):
#             print(i)
            sentence_idx = possible_types[i][0]
            sentence_type = possible_types[i][1]
            code = new_parse['sentences'][sentence_idx]['code']
            code = tuple(codeline.strip() for codeline in code)
            if code == possible_code:
                success = True
            if sentence_type != 'return':
                new_parse['sentences'][sentence_idx]['method'] = ['def '+sentence_type+'0(input_array):']
                new_parse['sentences'][sentence_idx]['code'] = possible_code
            else:
                new_parse['sentences'][sentence_idx]['code'] = possible_code[:-1] + (return_statement,)

#         if i > indexOf(possible_codes, code):
#             return False
        if check_solution(new_parse, fname):
            return True
        if success:
            return True
    print(False)
    return False

def check_problem(fname, problem_dir, sentence_dir, n, word_dir, m, p_thresh, tries):
#     success = True
    fnames = sorted(os.listdir(problem_dir))
    fnames = filter(lambda f: f != fname, fnames)
    translations_count = count_translations(problem_dir, fnames)
    fbase, fext = os.path.splitext(fname)
    with open(os.path.join(sentence_dir, fbase+'.label'), 'r') as inputjson:
        sentences_json = json.load(inputjson)
    with open(os.path.join(word_dir, fbase+'.label'), 'r') as inputjson:
        words_json = json.load(inputjson)
    with open(os.path.join(problem_dir, fname), 'r') as f:
        problem = f.read()
    parse = parse_problem(problem)
    possible_solutions = []
    possible_types = []
#     possible_solutions.append(parse)
#     possible_codeilnes = {}
    all_sentences = zip(sentences_json, words_json, parse['sentences'])
    for i, (sentence, word, sentence_parse) in enumerate(all_sentences):
        sentence_type = get_sentence_type(sentences_json, sentence, n)
#         print(sentence_type)
        if not sentence_type:
            continue
        possible_types.append((i, sentence_type))
        possible_codes = generate_possible_code(word,
                                                translations_count,
                                                p_thresh,
                                                sentence_parse)
#         print(len(list(possible_codes)))
#         code = tuple(codeline.strip() for codeline in sentence_parse['code'])
#         if code in possible_codes:
#             print(indexOf(possible_codes, code))
#         new_possible_solutions = []
        possible_solutions.append(possible_codes)
    print(possible_types)
    return check_solutions(possible_solutions, parse, possible_types, tries, fname)

# def gen_code(possible_codelines):
#     all_possible_code = product([type_codelines for codeline_type, type_codelines in possible_codelines.items()])


def check_problems(problem_dir, sentence_dir, n, word_dir, m, p_thresh, tries):
    fnames = sorted(os.listdir(problem_dir))
    correct = []
#     for each problem:
    for fname in fnames:
        print(fname)
        success = check_problem(fname, problem_dir, sentence_dir, n, word_dir, m, p_thresh, tries)
        if success:
            correct.append(fname)

#       generate code from words
    print(float(len(correct))/len(fnames))
    return correct

def clean_names(names):
    return [os.path.splitext(fname)[0] for fname in names]

def check_problems_intersection(sentence_dir, n, word_dir, m, problem_dir, p_thresh):
    sentence_score = problem2sentence.calc_score(sentence_dir, n)
    sentence_score = clean_names(sentence_score)

    word_score = sentence2word.calc_score(word_dir, m)
    word_score = clean_names(word_score)

    codeword_score = word2codeword.check_words(problem_dir, p_thresh)
    codeword_score = clean_names(codeword_score)

    codeline_score1 = codeline_gen.check_sentences(problem_dir)
    codeline_score1 = clean_names(codeline_score1)

#     codeline_score2 = codeline_gen_dep.check_sentences(problem_dir, 4)
#     codeline_score2 = [os.path.splitext(fname)[0] for fname in codeline_score2]

    s = ""
    for fname in sorted(clean_names(os.listdir(problem_dir))):
        base_pattern = "{:30} : {:10} {:10} {:10} {:10}\n"
        in_sentence = fname in sentence_score
        in_word = fname in word_score
        in_codeword = fname in codeword_score
        in_codeline = fname in codeline_score1
        s += base_pattern.format(fname, in_sentence, in_word, in_codeword, in_codeline)
    with open('res/intersection', 'w') as f:
        f.write(s)
    print(s)

#     print('wo dep: '+ str(set(problem_score).intersection(set(word_score)).intersection(set(codeword_score)).intersection(codeline_score1)))
    result = (set(sentence_score)\
        .intersection(set(word_score))\
        .intersection(set(codeword_score))\
        .intersection(set(codeline_score1)))
    return sorted(list(result))

def check_all_problems_intersection(sentence_dir, word_dir, problem_dir):
    sentence_score = {}
    for n in range(1,5):
        sentence_score = problem2sentence.calc_score(sentence_dir, n)
        sentence_score[n] = clean_names(sentence_score)

    word_score = {}
    for m in range(1,5):
        word_score = sentence2word.calc_score(word_dir, m)
        word_score[m] = clean_names(word_score)

    codeword_score = {}
    for p in range(1,6):
        p_thresh = p*0.1
        codeword_score = word2codeword.check_words(problem_dir, p_thresh)
        codeword_score[p] = clean_names(codeword_score)

    codeline_score1 = codeline_gen.check_sentences(problem_dir)
    codeline_score1 = clean_names(codeline_score1)

#     codeline_score2 = codeline_gen_dep.check_sentences(problem_dir, 4)
#     codeline_score2 = [os.path.splitext(fname)[0] for fname in codeline_score2]

#     print('wo dep: '+ str(set(problem_score).intersection(set(word_score)).intersection(set(codeword_score)).intersection(codeline_score1)))
    
    for n in range(1,5):
        for m in range(1,5):
            for p in range(1,6):
                s = ""
                for fname in sorted(clean_names(os.listdir(problem_dir))):
                    base_pattern = "{:30} : {:10} {:10} {:10} {:10}\n"
                    in_sentence = fname in sentence_score[n]
                    in_word = fname in word_score[m]
                    in_codeword = fname in codeword_score[p]
                    in_codeline = fname in codeline_score1
                    s += base_pattern.format(fname, in_sentence, in_word, in_codeword, in_codeline)
                with open('res/intersection'+'_'.join([n,m,p]), 'w') as f:
                    f.write(s)
                result = (set(sentence_score[n])\
                    .intersection(set(word_score[m]))\
                    .intersection(set(codeword_score[p]))\
                    .intersection(set(codeline_score1)))
                print('n:{} m:{} p:{} - {}'.format(n,m,p*0.1,len(result)))
    return 

if __name__ == '__main__':
    sentence_dir = 'res/sentence_json_small'
    n = 1
    word_dir = 'res/word_json_small'
    m = 2
#     problem_dir = 'res/problems_test'
    problem_dir = 'res/text&code5'
    p_thresh = 0.5
#     print(check_problems_intersection(sentence_dir, n, word_dir, m, problem_dir, p_thresh))
    check_all_problems_intersection(sentence_dir, word_dir, problem_dir)

    tries = 100000
#     print(check_problems(problem_dir, sentence_dir, n, word_dir, m, p_thresh, tries))

#     fname = 'AverageAverage.py'
#     fname = 'BlockTower.py'
#     fname = 'ChocolateBar.py'
#     fname = 'CompetitionStatistics.py'
#     fname = 'Elections.py'
#     print(check_problem(fname, problem_dir, sentence_dir, n, word_dir, m, p_thresh, tries))

#     fnames = sorted(os.listdir(problem_dir))
#     translations_count = count_translations(problem_dir, fnames)
#     print(translations_count)
#     print(word2codewords('tallest', translations_count))

#     with open(os.path.join(problem_dir, fname), 'r') as f:
#         problem = f.read()
#     parse = parse_problem(problem)
#     with open('temp.py', 'w') as f:
#         f.write(compose_problem(parse))
#     import temp
#     try:
#         result = temp.example0()
#         if result:
#             print('True')
#     except:
#         traceback.print_exc()
#     result = temp.example0()
#     print(result)
