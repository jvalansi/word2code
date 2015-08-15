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
from word2codeword import count_translations, word2codewords,\
    get_translation_dict
from problem_parser import parse_problem, compose_problem
from itertools import product, combinations
from codeline_gen import get_possible_codelines
import codeline_gen_dep
# from problem_utils import *
import numpy
import shutil
import copy
from utils import check_solution, clean_name
import problem_parser
from sentence2word import Sentence2Word
from problem2sentence import Problem2Sentence
import nltk

overwrite = True

golden_code = False #90%
golden_method = False #90%
golden_possibilities_codeline = True #10%
golden_codeline = False #50%
golden_return_codeline = True #10%
golden_sentence = True #10%
golden_words = True #10%
golden_codewords = True #10%

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

def get_expected_codeline(sentence_parse, word_type):
        type_codelines = set()
        for codeline in sentence_parse['code']:
            if sentence2word.get_type(nltk.word_tokenize(codeline)) == word_type:
                type_codelines.add((1.0, codeline))
        return type_codelines

def get_type_codelines(word_type, type_codewords):
    '''
    get all possible codelines according to word type and codewords
    
    :param word_type:
    :param type_codewords:
    '''
    type_codelines = set()
    if word_type != 'possibilities':
        type_codelines.add((0.1, word_type +' = lambda possibility: possibility'))
    for codeword_product in product(*type_codewords):
        if not codeword_product:
            continue
        for codeword_combination in combinations(codeword_product, min(len(codeword_product),2)):
#         codeword_combination = codeword_product
            probs, codewords = zip(*codeword_combination)
            p = numpy.prod(probs)
            codewords = list(codewords)
            if 'possibility' not in codewords: codewords.append('possibility')
            possible_codelines = get_possible_codelines(codewords)
            new_possible_codelines = set()
            for possible_codeline in possible_codelines:
                if word_type == 'possibilities':
                    possible_codeline = word_type + '= ' + possible_codeline
                else:
                    possible_codeline = word_type +' = lambda possibility: ' + possible_codeline
                new_possible_codelines.add(possible_codeline)
            possible_codelines = new_possible_codelines
            possible_codelines = [(p, type_codeline) for type_codeline in possible_codelines]
            type_codelines.update(possible_codelines)
    type_codelines = sorted(type_codelines, reverse=True)[:100]
    return type_codelines

possibilities_funcs = ['pairs', 'cpairs', 'subsets', 'csubsets', 'permutations', 'product', 'combinations_with_replacement', 'combinations'] 

def get_possibilities_codeline(sentence_parse, possible_types):
    if golden_possibilities_codeline:
        possibilities_codelines = get_expected_codeline(sentence_parse, 'possibilities')
    else:
        if possible_types[-1] == 'return':
            possibilities_codewords = [[(0.3, func) for func in ['subsets', 'csubsets']]]
        else:
            possibilities_codewords = [[(0.3, func) for func in ['pairs', 'cpairs']]]        
        possibilities_codelines = get_type_codelines('possibilities', possibilities_codewords)
    return possibilities_codelines

def get_return_codelines(sentence_parse, sentence_types):
    '''
    generate return codeline according to sentence type
    
    :param sentence_parse:
    :param sentence_types:
    '''
    if golden_return_codeline:
        return_codelines = get_expected_codeline(sentence_parse, 'return')
    else:
        return_codelines = set()
        inds, sentence_types = zip(*sentence_types)
        if not sentence_types or sentence_types[-1] != 'return':
            sentence_types = []
        valid0 = 'filter(valid0, ' if 'valid' in sentence_types else ''
        valid0_ = ')' if 'valid' in sentence_types else ''
        mapping0 = 'map(mapping0, ' if 'mapping' in sentence_types else ''
        mapping0_ = ')' if 'mapping' in sentence_types else ''
        reduce0 = 'reduce0(' if 'reduce' in sentence_types else ''
        reduce0_ = ')' if 'reduce' in sentence_types else ''
        base_pattern = 'return(reduce({}map(mapping, filter(valid, {}{} possibilities)))){}{}{}'
        return_codeline = base_pattern.format(reduce0, mapping0, valid0, valid0_, mapping0_, reduce0_)
        return_codelines.add((1.0, return_codeline))
        return_codeline = base_pattern.format(reduce0, valid0, mapping0, mapping0_, valid0_, reduce0_)
        return_codelines.add((1.0, return_codeline))
    return return_codelines


def generate_possible_code(sentence_json, m, translations_count, p, sentence_parse, sentence_types):
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
#     for translation, codeline in zip(sentence_parse['translations'], sentence_parse['code']):
#         codewords = nltk.word_tokenize(codeline)
#         type = codewords[0]
#         if type not in sentence2word.types:
#             continue
    for word_type in sentence2word.types:
#         if word_type in ['possibilities', 'return']:
        if word_type in ['return']:
            continue
        if sentence_types[-1][1] == 'possibilities' and word_type != 'possibilities':
            continue
        if (word_type != 'possibilities' and golden_codeline) or (word_type == 'possibilities' and golden_possibilities_codeline):
            type_codelines = get_expected_codeline(sentence_parse, word_type)
            if not type_codelines:
                if word_type == 'possibilities':
                    type_codelines.add((0.5, 'pass'))
                elif word_type == 'valid':
                    type_codelines.add((1.0, word_type +' = lambda possibility: True'))
#                     type_codelines.add((1.0, word_type +' = lambda possibility: possibility'))
                else:
                    type_codelines.add((1.0, word_type +' = lambda possibility: possibility'))
            possible_codes.append(type_codelines)
            continue
        if golden_words:
            type_words = Sentence2Word().get_expected_label_words(sentence_json, word_type)
            print(type_words)
        else:
            type_words = Sentence2Word().get_probable_label_words(sentence_json, word_type, m)
        if golden_codewords:
            transdict = get_translation_dict(sentence_parse['translations'], sentence_parse['code'], stem=False)
            type_codewords = [[(1.0, transdict[word])] for word in type_words]
        else:
            type_codewords = [word2codewords(word, translations_count, p=p) for word in type_words]
#             if word_type != 'possibilities':
#                 type_codewords = [[(prob,word) for prob,word in word_codewords if word not in possibilities_funcs] for word_codewords in type_codewords]
        type_codelines = get_type_codelines(word_type, type_codewords)
#         type_codelines = get_type_codelines(word_type, [])
#         if codeline.strip() not in type_codelines:
#             print(False)
        possible_codes.append(type_codelines)
    if sentence_types[-1][1] != 'possibilities':
        return_codelines = get_return_codelines(sentence_parse, sentence_types)
    #     return_codelines.add((1.0, 'return(reduce(map(mapping, filter(valid, possibilities(input_array)))))'))
        possible_codes.append(return_codelines)
    if not possible_codes:
        return []
    product_code = []
    for possible_code in product(*possible_codes):
        probs, codes = zip(*possible_code)
        p = numpy.prod(probs)
        product_code.append((p, codes))
    product_code = sorted(product_code, reverse=True)[:100]
    product_code = [code for p, code in product_code]
    return product_code

def check_solutions(problem_parse, possible_types, possible_solutions, tries, indir, fname, solutions_dir):
    '''
    check possible solutions to find whether they solve the problem
    
    :param problem_parse:
    :param possible_types:
    :param possible_solutions:
    :param tries:
    :param fname:
    '''
    print('check_solutions')
    sol_dir = solutions_dir
    if not os.path.exists(sol_dir):
        os.mkdir(sol_dir)
    fpath = os.path.join(sol_dir, fname)
#     return_statement = build_return(possible_types)
    preprocessed_parse = copy.deepcopy(problem_parse)
    for possible_type in possible_types:
        sentence_idx = possible_type[0]
        sentence_type = possible_type[1]
        if sentence_type in ['return', 'possibilities']:
            continue
        if not golden_method:
            preprocessed_parse['sentences'][sentence_idx]['method'] = ['def '+sentence_type+'0(possibility):']
    for sentence_parse in preprocessed_parse['sentences']:
        sentence_parse['code'] = []
    for j, possible_codes in enumerate(product(* possible_solutions)):
        if not j%1000:
            print(j)
        if j > tries:
            return False
#         new_parse = copy.deepcopy(preprocessed_parse)
        success = False
        for i, possible_code in enumerate(possible_codes):
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

def check_problem(fname, problem_dir, sentence_dir, n, word_dir, m, p, tries, solutions_dir):
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
    if not overwrite and fname in os.listdir(solutions_dir):
        return
    fnames = sorted(os.listdir(problem_dir))
    fnames = filter(lambda f: f != fname, fnames)
    translations_count = count_translations(problem_dir, fnames)
    sentence_fpath = os.path.join(sentence_dir, clean_name(fname)+'.json')
    if not os.path.exists(sentence_fpath):
        return
    with open(sentence_fpath, 'r') as inputjson:
        sentences_json = json.load(inputjson)
    word_fpath = os.path.join(word_dir, clean_name(fname)+'.json')
    if not os.path.exists(word_fpath):
        return
    with open(word_fpath, 'r') as inputjson: #TODO: fix ext
        words_json = json.load(inputjson)
    with open(os.path.join(problem_dir, fname), 'r') as f:
        problem = f.read()
    problem_parse = parse_problem(problem)
    possible_solutions = []
    possible_types = []
    all_sentences = zip(sentences_json, words_json, problem_parse['sentences'])
    for i, (sentence_json, word_json, sentence_parse) in enumerate(all_sentences):
        print(i)
        if golden_sentence:
            sentence_type = Problem2Sentence().get_expected_sentence_label(sentence_json)
        else:
            sentence_type = Problem2Sentence().get_probable_sentence_label(sentences_json, sentence_json, n)
        print(sentence_type)
        if not sentence_type:
            continue
        possible_types.append((i, sentence_type)) #TODO: maybe only sentence_type
        if golden_code:
            possible_codes = [sentence_parse['code']]
        else:
            possible_codes = generate_possible_code(word_json,
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
    print(possible_types)
    return check_solutions(problem_parse, possible_types, possible_solutions, tries, problem_dir, fname, solutions_dir)

# def gen_code(possible_codelines):
#     all_possible_code = product([type_codelines for codeline_type, type_codelines in possible_codelines.items()])

def check_problems(problem_dir, sentence_dir, n, word_dir, m, p_thresh, tries, solutions_dir):
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
    :param solutions_dir:
    '''
    correct = []
    total = 0
#     for each problem:
    for fname in sorted(os.listdir(problem_dir)):
        if not fname.endswith('.py'):
            continue
        if not check_solution(os.path.join(problem_dir, fname)):
            continue
        print(fname)
        success = check_problem(fname, problem_dir, sentence_dir, n, word_dir, m, p_thresh, tries, solutions_dir)
        if success:
            correct.append(fname)
        total += 1
#       generate code from words
    print(len(correct))
    print(total)
    print(float(len(correct))/total)
    return correct

def check_all_problems_intersection(sentence_dir, N, word_dir, M, problem_dir, P, intersections_path, all_range=True):
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
    if all_range:
        N0 = M0 = P0 = 1
    else:
        N0 = N-1
        M0 = M-1
        P0 = P-1
    sentence_score = {}
    for n in range(N0,N):
        sentence_score[n] = Problem2Sentence().calc_score(sentence_dir, n)
        sentence_score[n] = map(clean_name, sentence_score[n])

    word_score = {}
    for m in range(M0,M):
        word_score[m] = Sentence2Word().calc_score(word_dir, m)
        word_score[m] = map(clean_name, word_score[m])

    codeword_score = {}
    for p in range(P0,P):
        p_thresh = p
        codeword_score[p] = word2codeword.check_words(problem_dir, p_thresh)
        codeword_score[p] = map(clean_name, codeword_score[p])

#     codeline_score1 = codeline_gen.check_sentences(problem_dir)
#     codeline_score1 = map(clean_name, codeline_score1)

#     codeline_score2 = codeline_gen_dep.check_sentences(problem_dir, 4)
#     codeline_score2 = [os.path.splitext(fname)[0] for fname in codeline_score2]

#     print('wo dep: '+ str(set(problem_score).intersection(set(word_score)).intersection(set(codeword_score)).intersection(codeline_score1)))
    summary = ""
    if all_range and os.path.exists(intersections_path):
        shutil.rmtree(intersections_path)
    if not os.path.exists(intersections_path):
        os.mkdir(intersections_path)        
    summary += ' '.join(['{}: {}'.format(k, len(v)) for k, v in sentence_score.items()]) + '\n'
    summary += ' '.join(['{}: {}'.format(k, len(v)) for k, v in word_score.items()]) + '\n'
    summary += ' '.join(['{}: {}'.format(k, len(v)) for k, v in codeword_score.items()]) + '\n'
    for n,m,p in product(range(N0,N),range(M0,M),range(P0,P)):
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
        summary += 'n:{} m:{} p:{} - {}\n'.format(n,m,p,len(result))
    if all_range:
        with open(os.path.join(intersections_path, 'summary'), 'w') as f:
            f.write(summary)

def main():
#     problem_dir = os.path.join('res', 'problems_test1')
    problem_dir = os.path.join('res', 'text&code8')
#     p_thresh = 0.5
    p = 1
    sentence_dir = os.path.join(problem_dir, 'sentence_json')
    n = 1
    word_dir = os.path.join(problem_dir, 'word_json')
#     word_dir = os.path.join(problem_dir, 'word_json_struct')
    word_dir = os.path.join(problem_dir, 'word_test_json')
    m = 2

    intersections_path = os.path.join(problem_dir, 'intesections')
    N = M = P = 4
#     check_all_problems_intersection(sentence_dir, N, word_dir, M, problem_dir, P, intersections_path)
    
    tries = 10000
    solutions_dir = os.path.join(problem_dir, 'solutions_return')
    success1 = (check_problems(problem_dir, sentence_dir, n, word_dir, m, p, tries, solutions_dir))
    global golden_return_codeline
    golden_return_codeline = False
    solutions_dir = os.path.join(problem_dir, 'solutions')
    success2 = (check_problems(problem_dir, sentence_dir, n, word_dir, m, p, tries, solutions_dir))
    print(success1)
    print(success2)
    print(sorted(set(success2).difference(success1)))

#     results = []
#     for fname in sorted(os.listdir(solutions_dir)):
#         if not fname.endswith('.py'):
#             continue
#         print(fname)
#         problem_path = os.path.join(solutions_dir, fname)
#         if not check_solution(problem_path):
#             results.append(fname)
#     print(results)

#     fname = 'AmoebaDivTwo.py'
#     fname = 'BlockTower.py'
#     fname = 'ChocolateBar.py'
    fname = 'CompetitionStatistics.py'
#     fname = 'Elections.py'
    fname = 'SwappingDigits.py'
#     fname = 'TheEquation.py'
    fname = 'IdentifyingWood.py'
    fname = 'PalindromesCount.py'
#     fname = 'FibonacciDiv2.py'
    fname = 'AlienAndPassword.py'
#     fname = 'AverageAverage.py'
#     fname = 'BasketsWithApples.py'
#     print(check_problem(fname, problem_dir, sentence_dir, n, word_dir, m, p, tries, solutions_dir))
#     fpath = os.path.join(solutions_dir, fname)
#     print(check_solution(fpath))
    
#     fnames = sorted(os.listdir(problem_dir))
#     translations_count = count_translations(problem_dir, fnames)
#     print(translations_count)
#     print(word2codewords('tallest', translations_count))

if __name__ == '__main__':
    main()