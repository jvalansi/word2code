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
from problem2sentence import get_possible_sentence_type
from word2codeword import count_translations, word2codewords
from problem_parser import parse_problem, compose_problem
from itertools import product, combinations
from codeline_gen import get_possible_codelines
import codeline_gen_dep
# from problem_utils import *
import numpy
import shutil
import copy
from utils import check_solution
from sentence2word import get_probable_label_words

#     phrase to code:
#     phrase:         Return the number of different passwords Fred needs to try.
#     dependencies:    det(number-3, the-2)
#                      prep_return(needs-8, number-3)
#                      amod(passwords-6, different-5)
#                      prep_of(number-3, passwords-6)
#                      nsubj(needs-8, Fred-7)
#                      nsubj(try-10, Fred-7)
#                      root(ROOT-0, needs-8)
#                      aux(try-10, to-9)
#                      xcomp(needs-8, try-10)
#                     return(number(different(passwords(needs(Fred,try)))
#                     return(number(different(possibility for possibility in passwords if valid(possibility))))
#     code:           return(len(set(possibility for possibility in possibilities if valid(possibility))))
#
#     phrase:         the correct array can be done from S by removing exactly 1 element
#                     det(array-3, the-1)
#                     amod(array-3, correct-2) correct = lambda array:
#                     nsubjpass(done-6, array-3)
#                     aux(done-6, can-4)
#                     auxpass(done-6, be-5)
#                     root(ROOT-0, done-6)
#                     prep_from(done-6, S-8)
#                     agent(done-6, removing-10)
#                     advmod(element-13, exactly-11)
#                     num(element-13, 1-12)
#                     dobj(removing-10, element-13) - removing
#     ROOT(done(array(correct),S,removing(element(exactly,1)))
#     ####    correct = lambda array: exactly(len(removing(S, array)), 1)
#     code:   valid = lambda possibility: eq(len(diff(input_array, possibility)), 1)
#
#     every cell of the table covered by the amoeba must only contain antimatter.
#                     det(cell-2, every-1)
#                     nsubj(contain-12, cell-2)
#                     det(table-5, the-4)
#                     prep_of(cell-2, table-5)
#                     vmod(table-5, covered-6)
#                     det(amoeba-9, the-8)
#                     agent(covered-6, amoeba-9)
#                     aux(contain-12, must-10)
#                     advmod(contain-12, only-11)
#                     root(ROOT-0, contain-12)
#                     dobj(contain-12, antimatter-13)
#     ROOT(contain(cell(every,table(covered(amoeba)),must,only,antimatter)))
#     ####    valid = lambda amoeba:     every(contain(cell, antimatter[0]) for cell of table if covered(cell, amoeba))
#             valid = lambda possibility: all(contains(element, types[0]) for element in input_array if contains(element, possibility))


def get_type_codelines(word_type, type_codewords):
    '''
    get all possible codelines according to word type and codewords
    
    :param word_type:
    :param type_codewords:
    '''
    type_codelines = set()
    type_codelines.add((0.1, word_type +' = lambda possibility: possibility'))
    for codeword_product in product(*type_codewords):
        if not codeword_product:
            continue
        for codeword_combination in combinations(codeword_product, 1):
#         codeword_combination = codeword_product
            probs, codewords = zip(*codeword_combination) 
            p = numpy.prod(probs)
            if 'possibility' not in codewords: codewords.append('possibility')
            possible_codelines = get_possible_codelines(codewords)
            new_possible_codelines = set()
            for possible_codeline in possible_codelines:
                possible_codeline = word_type +' = lambda possibility: ' + possible_codeline
                new_possible_codelines.add(possible_codeline)
            possible_codelines = new_possible_codelines
            possible_codelines = [(p, type_codeline) for type_codeline in possible_codelines]
            type_codelines.update(possible_codelines)
    type_codelines = sorted(type_codelines, reverse=True)[:100]
    return type_codelines

possibilities_funcs = ['pairs', 'cpairs', 'subsets', 'csubsets'] 

def get_return_codeline(types):
    '''
    generate return codeline according to sentence type
    
    :param types:
    '''
    if not types or types[-1] != 'return':
        types = []
    else: 
        inds, types = zip(*types)
    valid0 = 'filter(valid0, ' if 'valid' in types else ''
    valid0_ = ')' if 'valid' in types else ''
    mapping0 = 'map(mapping0, ' if 'mapping' in types else ''
    mapping0_ = ')' if 'mapping' in types else ''
    reduce0 = 'reduce0(' if 'reduce' in types else ''
    reduce0_ = ')' if 'reduce' in types else ''
    base_pattern = 'return({}reduce(map(mapping, filter(valid, {}{} possibilities(input_array))))){}{}{}'
    return base_pattern.format(reduce0, mapping0, valid0, valid0_, mapping0_, reduce0_)

def generate_possible_code(sentence_json, m, translations_count, p, sentence_parse, possible_types):
    '''
    generate all possible code for sentence 
    
    :param sentence_json:
    :param m: number of possible words for each type 
    :param translations_count:
    :param p: number of possible codewords for each word
    :param sentence_parse:
    :param possible_types: possible sentence types
    '''
    possible_codes = []
    possibilities_codelines = set()
    for func in possibilities_funcs:
        possible_codelines =  get_possible_codelines([func], 'possibilities')
        possible_codelines = [(1.0, codeline) for codeline in possible_codelines]
        possibilities_codelines.update(possible_codelines)
    possible_codes.append(possibilities_codelines)
#     for translation, codeline in zip(sentence_parse['translations'], sentence_parse['code']):
#         codewords = nltk.word_tokenize(codeline)
#         type = codewords[0]
#         if type not in sentence2word.types:
#             continue
    for word_type in sentence2word.types:
        type_words = get_probable_label_words(sentence_json, word_type, m)
        type_codewords = [word2codewords(word, translations_count, p=p) for word in type_words]
        type_codelines = get_type_codelines(word_type, type_codewords)
#         type_codelines = get_type_codelines(word_type, [])
#         if codeline.strip() not in type_codelines:
#             print(False)
        possible_codes.append(type_codelines)
    return_codelines = set()
    return_codeline = get_return_codeline(possible_types)
    return_codelines.add((1.0, return_codeline))
#     return_codelines.add((1.0, 'return(reduce(map(mapping, filter(valid, possibilities(input_array)))))'))
    possible_codes.append(return_codelines)
    product_code = []
    for possible_code in product(*possible_codes):
        probs, codes = zip(*possible_code)
        p = numpy.prod(probs)
        product_code.append((p, codes))
    product_code = sorted(product_code, reverse=True)[:100]
    product_code = [code for p, code in product_code]
    return product_code

def check_solutions(problem_parse, possible_types, possible_solutions, tries, fname):
    '''
    check possible solutions to find whether they solve the problem
    
    :param problem_parse:
    :param possible_types:
    :param possible_solutions:
    :param tries:
    :param fname:
    '''
    print('check_solutions')
    sol_dir = os.path.join('res','solutions')
    if not os.path.exists(sol_dir):
        os.mkdir(sol_dir)
    fpath = os.path.join(sol_dir, fname)
#     return_statement = build_return(possible_types)
    preprocessed_parse = copy.deepcopy(problem_parse)
    for possible_type in possible_types:
        sentence_idx = possible_type[0]
        sentence_type = possible_type[1]
        if sentence_type == 'return':
            continue
        preprocessed_parse['sentences'][sentence_idx]['method'] = ['def '+sentence_type+'0(input_array):']
    for sentence_parse in preprocessed_parse['sentences']:
        sentence_parse['code'] = []
    for j, possible_codes in enumerate(product(* possible_solutions)):
#         if not j%1000:
        print(j)
        if j > tries:
            return False
#         new_parse = copy.deepcopy(preprocessed_parse)
        success = False
        for i, possible_code in enumerate(possible_codes):
#             print(i)
            sentence_idx = possible_types[i][0]
            sentence_type = possible_types[i][1]
#             code = preprocessed_parse['sentences'][sentence_idx]['code']
#             code = tuple(codeline.strip() for codeline in code)
#             if code == possible_code:
#                 success = True
#             if sentence_type != 'return':
#                 new_parse['sentences'][sentence_idx]['method'] = ['def '+sentence_type+'0(input_array):']
#                 new_parse['sentences'][sentence_idx]['code'] = possible_code
#             else:
#                 new_parse['sentences'][sentence_idx]['code'] = possible_code[:-1] + (return_statement,)
            preprocessed_parse['sentences'][sentence_idx]['code'] = possible_code
#         if i > indexOf(possible_codes, code):
#             return False
        with open(fpath, 'w') as f:
            f.write(compose_problem(preprocessed_parse))
        if check_solution(fpath):
            return True
        if success:
            return True
    print(False)
    return False

def check_problem(fname, problem_dir, sentence_dir, n, word_dir, m, p, tries):
    '''
    check problem:
        find sentence types and possible code
        check whether the code wolves the given problem
    
    :param fname: problem name
    :param problem_dir: path to problems
    :param sentence_dir: path to senteces json
    :param n: number of possible sentences for each type
    :param word_dir: path to words json
    :param m: number of possible words for each type 
    :param p: number of possible codewords for each word
    :param tries: maximal number of solutions to check
    '''
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
    problem_parse = parse_problem(problem)
    possible_solutions = []
    possible_types = []
    all_sentences = zip(sentences_json, words_json, problem_parse['sentences'])
    for i, (sentence, word, sentence_parse) in enumerate(all_sentences):
        print(i)
        sentence_type = get_possible_sentence_type(sentences_json, sentence, n)
        if not sentence_type:
            continue
        possible_types.append((i, sentence_type))
        possible_codes = generate_possible_code(word,
                                                m,
                                                translations_count,
                                                p,
                                                sentence_parse,
                                                possible_types)
#         possible_codes = []
#         print(len(list(possible_codes)))
#         code = tuple(codeline.strip() for codeline in sentence_parse['code'])
#         if code in possible_codes:
#             print(indexOf(possible_codes, code))
#         new_possible_solutions = []
        possible_solutions.append(possible_codes)
    return check_solutions(problem_parse, possible_types, possible_solutions, tries, fname)

# def gen_code(possible_codelines):
#     all_possible_code = product([type_codelines for codeline_type, type_codelines in possible_codelines.items()])

def check_problems(problem_dir, sentence_dir, n, word_dir, m, p_thresh, tries):
    '''
    check all the problem in the problem dir
    for each problem:
        find sentence types and possible code
        check whether the code wolves the given problem
    
    :param problem_dir: path to problems
    :param sentence_dir: path to senteces json
    :param n: number of possible sentences for each type
    :param word_dir: path to words json
    :param m: number of possible words for each type 
    :param p: number of possible codewords for each word
    :param tries: maximal number of solutions to check
    '''
    fnames = sorted(os.listdir(problem_dir))
    correct = []
#     for each problem:
    for fname in fnames:
        if not fname.endswith('.py'):
            continue
        print(fname)
        success = check_problem(fname, problem_dir, sentence_dir, n, word_dir, m, p_thresh, tries)
        if success:
            correct.append(fname)
#       generate code from words
    print(float(len(correct))/len(fnames))
    return correct

def clean_name(fname):
    return os.path.splitext(fname)[0]

def check_problems_intersection(sentence_dir, n, word_dir, m, problem_dir, p):
    '''
    check the intersections of correctness of each of the stages:
        sentence type extraction
        word type extraction
        codeword extraction
    
    :param sentence_dir: path to senteces json
    :param n: number of possible sentences for each type
    :param word_dir: path to words json
    :param m: number of possible words for each type 
    :param problem_dir: path to problems
    :param p: number of possible codewords for each word
    '''
    sentence_score = problem2sentence.calc_score(sentence_dir, n)
    sentence_score = map(clean_name, sentence_score)

    word_score = sentence2word.calc_score(word_dir, m)
    word_score = map(clean_name, word_score)

    codeword_score = word2codeword.check_words(problem_dir, p)
    codeword_score = map(clean_name, codeword_score)

    codeline_score1 = codeline_gen.check_sentences(problem_dir)
    codeline_score1 = map(clean_name, codeline_score1)

#     codeline_score2 = codeline_gen_dep.check_sentences(problem_dir, 4)
#     codeline_score2 = [os.path.splitext(fname)[0] for fname in codeline_score2]

    s = ""
    for fname in sorted(os.listdir(problem_dir)):
        fname = clean_name(fname)
        base_pattern = "{:30} : {:10} {:10} {:10} {:10}\n"
        in_sentence = fname in sentence_score
        in_word = fname in word_score
        in_codeword = fname in codeword_score
        in_codeline = fname in codeline_score1
        s += base_pattern.format(fname, in_sentence, in_word, in_codeword, in_codeline)
    with open('res/intersection', 'w') as f:
        f.write(s)
#     print(s)

#     print('wo dep: '+ str(set(problem_score).intersection(set(word_score)).intersection(set(codeword_score)).intersection(codeline_score1)))
    result = (set(sentence_score)\
        .intersection(set(word_score))\
        .intersection(set(codeword_score))\
        .intersection(set(codeline_score1)))
    return sorted(list(result))

def check_all_problems_intersection(sentence_dir, word_dir, problem_dir, intersections_path):
    '''
    check the intersections of correctness of each of the stages:
        sentence type extraction
        word type extraction
        codeword extraction
    for each number of possibilities up to N,M,P respectively
    
    :param sentence_dir: path to senteces json
    :param word_dir: path to words json
    :param problem_dir: path to problems
    :param intersections_path: path to write calculated intersection
    '''
    sentence_score = {}
    N = M = P = 5 
    for n in range(1,N):
        sentence_score[n] = problem2sentence.calc_score(sentence_dir, n)
        sentence_score[n] = map(clean_name, sentence_score[n])

    word_score = {}
    for m in range(1,M):
        word_score[m] = sentence2word.calc_score(word_dir, m)
        word_score[m] = map(clean_name, word_score[m])

    codeword_score = {}
    for p in range(1,P):
        p_thresh = p
        codeword_score[p] = word2codeword.check_words(problem_dir, p_thresh)
        codeword_score[p] = map(clean_name, codeword_score[p])

#     codeline_score1 = codeline_gen.check_sentences(problem_dir)
#     codeline_score1 = map(clean_name, codeline_score1)

#     codeline_score2 = codeline_gen_dep.check_sentences(problem_dir, 4)
#     codeline_score2 = [os.path.splitext(fname)[0] for fname in codeline_score2]

#     print('wo dep: '+ str(set(problem_score).intersection(set(word_score)).intersection(set(codeword_score)).intersection(codeline_score1)))
    summary = ""
    if os.path.exists(intersections_path):
        shutil.rmtree(intersections_path)
    os.mkdir(intersections_path)
    summary += ' '.join(['{}: {}'.format(k, len(v)) for k, v in sentence_score.items()]) + '\n'
    summary += ' '.join(['{}: {}'.format(k, len(v)) for k, v in word_score.items()]) + '\n'
    summary += ' '.join(['{}: {}'.format(k, len(v)) for k, v in codeword_score.items()]) + '\n'
    for n,m,p in product(range(1,N),range(1,M),range(1,P)):
        s = ""
        for fname in sorted(os.listdir(problem_dir)):
            if not fname.endswith('py'):
                continue
            fpath = os.path.join(problem_dir, fname)
            if not check_solution(fpath):
                continue  
            fname = clean_name(fname)
            base_pattern = "{:30} : {:10} {:10} {:10}\n"
            in_sentence = fname in sentence_score[n]
            in_word = fname in word_score[m]
            in_codeword = fname in codeword_score[p]
#                     in_codeline = fname in codeline_score1
#                     s += base_pattern.format(fname, in_sentence, in_word, in_codeword, in_codeline)
            s += base_pattern.format(fname, in_sentence, in_word, in_codeword)
        fname = 'intersection_{}_{}_{}'.format(n,m,p)
        with open(os.path.join(intersections_path, fname), 'w') as f:
            f.write(s)
        result = (set(sentence_score[n])\
            .intersection(set(word_score[m]))\
            .intersection(set(codeword_score[p])))
#                     .intersection(set(codeline_score1)))
#                 print(sentence_score[n])
#                 print(word_score[m])
#                 print(codeword_score[p])
        summary += 'n:{} m:{} p:{} - {}\n'.format(n,m,p,len(result))
    with open(os.path.join(intersections_path, 'summary'), 'w') as f:
        f.write(summary)
    return 

def main():
    problem_dir = os.path.join('res', 'problems_test')
    problem_dir = os.path.join('res', 'text&code5')
    problem_dir = os.path.join('res', 'text&code6')
#     p_thresh = 0.5
    p = 1
    sentence_dir = os.path.join(problem_dir, 'sentence_json')
#     sentence_dir = 'res/sentence_json_small'
    n = 1
#     word_dir = 'res/word_json'
    word_dir = os.path.join(problem_dir, 'word_json')
#     word_dir = 'res/word_json_small'
    m = 1
#     print(check_problems_intersection(sentence_dir, n, word_dir, m, problem_dir, p_thresh))

    intersections_path = os.path.join(problem_dir, 'intesections')
    check_all_problems_intersection(sentence_dir, word_dir, problem_dir, intersections_path)
    
    tries = 100000
#     print(check_problems(problem_dir, sentence_dir, n, word_dir, m, p_thresh, tries))
#     print(check_problems(problem_dir, sentence_dir, n, word_dir, m, p, tries))

#     fname = 'AmoebaDivTwo.py'
#     fname = 'AverageAverage.py'
#     fname = 'BlockTower.py'
    fname = 'ChocolateBar.py'
#     fname = 'CompetitionStatistics.py'
#     fname = 'Elections.py'
#     print(check_problem(fname, problem_dir, sentence_dir, n, word_dir, m, p, tries))

#     fnames = sorted(os.listdir(problem_dir))
#     translations_count = count_translations(problem_dir, fnames)
#     print(translations_count)
#     print(word2codewords('tallest', translations_count))

if __name__ == '__main__':
    main()