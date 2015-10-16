'''
Created on Apr 28, 2015

@author: jordan
'''
import os
import problem2sentence
import sentence2word
import word2codeword
import codeline_gen
import codeline_gen_dep
import json
from word2codeword import count_translations, word2codewords,\
    get_translation_dict
from problem_parser import parse_problem, compose_problem
from itertools import product, combinations
# from codeline_gen import get_possible_codelines
from codeline_gen_dep import get_possible_codelines
# from problem_utils import *
import numpy
import shutil
import copy
from utils import check_solution, clean_name, codeline_types, get_codeline_type,\
    add_codeline_prefix, clean_codeline, draw, show, check_solution_path
import problem_parser
from sentence2word import Sentence2Word
from problem2sentence import Problem2Sentence
import nltk
from dependency_parser import Node, translate_code

overwrite = True

# 92% for all true
golden_sentence = True #46% for False
golden_method = True #85% for False
golden_code = False #87% for False 

golden_possibilities_codeline = True #10%
golden_codeline = False #50%
golden_return_codeline = True #66% for False

golden_words = False #10%
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

def get_default_codeline(word_type):
    type_codelines = set()
    if word_type == 'possibilities':
        type_codelines.add((0.5, 'pass'))
    elif word_type == 'valid':
        type_codelines.add((1.0, word_type +' = lambda possibility: True'))
#                 type_codelines.add((1.0, word_type +' = lambda possibility: possibility'))
    else:
        type_codelines.add((1.0, word_type +' = lambda possibility: possibility'))
    return type_codelines

def get_expected_codeline(code, word_type):
        type_codelines = set()
        for codeline in code:
            if get_codeline_type(codeline) == word_type:
                type_codelines.add((1.0, codeline))
        if not type_codelines:
            type_codelines = get_default_codeline(word_type)
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


def get_type_codelines(word_type, type_codewords, var_codewords, transdict, sentence, sentence_type):
    '''
    get all possible codelines according to word type and codewords
    
    :param word_type:
    :param type_codewords:
    '''
    type_codelines = set()
    all_codewords = type_codewords + var_codewords
    for codeword_product in product(*all_codewords):
        if not codeword_product:
            continue
        funcwords = codeword_product[:len(type_codewords)]
        if not funcwords:
            continue
        varwords = codeword_product[len(type_codewords):]
        if varwords:
            probs, varwords = zip(*varwords)
        for funcwords_combination in combinations(funcwords, min(len(funcwords),2)):
#         codeword_combination = codeword_product
            probs, codewords = zip(*funcwords_combination)
            p = numpy.prod(probs)
#             possible_codelines = get_possible_codelines(codewords)
            codewords = list(codewords) + list(varwords)
            possible_codelines = []
            subtransdict = {k:v for k,v in transdict.items() if v in codewords and v != "input_array"}
            possible_codelines = get_possible_codelines(sentence, subtransdict, sentence_type, word_type)
            subtransdict = {k:v for k,v in transdict.items() if v in codewords}
            possible_codelines.extend(get_possible_codelines(sentence, subtransdict, sentence_type, word_type)) #TODO: fix duplicate
#             possible_codelines = get_possible_codelines(codewords)
            possible_codelines = [add_codeline_prefix(codeline, word_type) for codeline in possible_codelines]
            possible_codelines = [(p, type_codeline) for type_codeline in possible_codelines]
            type_codelines.update(possible_codelines)
    if not type_codelines:
        type_codelines = get_default_codeline(word_type)
    type_codelines = sorted(type_codelines, reverse=True)[:100]
    return type_codelines

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

def get_combinations(possible_codes):
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

def to_dict(words, codewords):
    return {codeword: word for word,word_codewords in zip(words, codewords) for p,codeword in word_codewords}

def generate_possible_code(sentence_json, M, translations_count, P, sentence_parse, sentence_types):
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
    possible_tranlations = []
    if golden_words:
        var_words = Sentence2Word().get_expected_label_words(sentence_json, 'var')
    else:
        var_words = Sentence2Word().get_probable_label_words(sentence_json, 'var', M)
    if golden_codewords:
        golden_transdict = get_translation_dict(sentence_parse['translations'], sentence_parse['code'], stem=False)
        var_codewords = [[(1.0, golden_transdict[word])] for word in var_words if word in golden_transdict] #TODO: remove filter (should all be in dict)
    else:
        var_codewords = [word2codewords(word, translations_count, p=P) for word in var_words]
    vartransdict = to_dict(var_words, var_codewords)
    varcodedict = {v:k for v,k in vartransdict.items()}
    for word_type in codeline_types:
        print(word_type)
#         if word_type in ['possibilities', 'return']:
        if word_type in ['return']:
            continue
        if sentence_types[-1][1] == 'possibilities' and word_type != 'possibilities':
            continue
        if (word_type != 'possibilities' and golden_codeline) or (word_type == 'possibilities' and golden_possibilities_codeline):
            type_translations = get_expected_codeline(sentence_parse['translations'], word_type)
            type_codelines = get_expected_codeline(sentence_parse['code'], word_type)
        else:
            if golden_words:
                type_words = Sentence2Word().get_expected_label_words(sentence_json, word_type)
            else:
                type_words = Sentence2Word().get_probable_label_words(sentence_json, word_type, M)
#             print(type_words)
            if golden_codewords:
                type_codewords = [[(1.0, golden_transdict[word])] for word in type_words if word in golden_transdict] #TODO: remove filter (should all be in dict)
            else:
                type_codewords = [word2codewords(word, translations_count, p=P) for word in type_words]
#             print(type_codewords)
    #             if word_type != 'possibilities':
    #                 type_codewords = [[(prob,word) for prob,word in word_codewords if word not in possibilities_funcs] for word_codewords in type_codewords]
            codedict = to_dict(type_words, type_codewords)
            codedict.update(varcodedict)
            transdict = {v:k for k,v in codedict.items()}
            print(codedict)
            type_codelines = get_type_codelines(word_type, type_codewords, var_codewords, transdict, sentence_parse['sentence'], sentence_types[-1][1])
            print(type_codelines)
            clean_codelines = [(prob,clean_codeline(type_codeline)) for prob,type_codeline in type_codelines]
            type_translations = [(prob,translate_code(codeline, codedict)) for prob,codeline in clean_codelines]
            type_translations = [(prob,add_codeline_prefix(translation, word_type)) for prob,translation in type_translations]             
        possible_tranlations.append(type_translations)
        possible_codes.append(type_codelines)
    if sentence_types[-1][1] != 'possibilities':
        return_codelines = get_return_codelines(sentence_parse['code'], sentence_types)
    #     return_codelines.add((1.0, 'return(reduce(map(mapping, filter(valid, possibilities(input_array)))))'))
        possible_tranlations.append(return_codelines)
        possible_codes.append(return_codelines)
    product_code = get_combinations(possible_codes)
    product_translation = get_combinations(possible_tranlations)
    return zip(product_code, product_translation) 

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
    fpath = os.path.join(solutions_dir, clean_name(fname))
    if not os.path.exists(fpath):
        os.mkdir(fpath)
    good_fpath = os.path.join(fpath,'Good')
    if os.path.exists(good_fpath):
        shutil.rmtree(good_fpath)
    os.mkdir(good_fpath)
    bad_fpath = os.path.join(fpath,'Bad')
    if os.path.exists(bad_fpath):
        shutil.rmtree(bad_fpath)
    os.mkdir(bad_fpath)
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
    for j, possible_solution in enumerate(product(* possible_solutions)):
        if not j%1000:
            print(j)
        if j > tries:
            return False
        for i, (possible_code, possible_translation) in enumerate(possible_solution):
            sentence_idx, sentence_type = possible_types[i]
            preprocessed_parse['sentences'][sentence_idx]['code'] = possible_code
            preprocessed_parse['sentences'][sentence_idx]['translations'] = possible_translation
        sol_fname = os.path.join(good_fpath, str(j)+'.py')
        with open(sol_fname, 'w') as f:
            f.write(compose_problem(preprocessed_parse))
        if check_solution(sol_fname):
            print(True)
        else:
            shutil.move(sol_fname, bad_fpath)
    print(False)

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
    if not os.path.exists(solutions_dir):
        os.mkdir(solutions_dir)
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
            possible_codes = zip([sentence_parse['code']], [sentence_parse['translation']])
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

def check_all_problems_intersection(sentence_dir, N, word_dir, M, problem_dir, P, intersections_path, Q=4, all_range=True):
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
        N0 = M0 = P0 = Q0 = 1
    else:
        N0 = N-1
        M0 = M-1
        P0 = P-1

    total = check_solution_path(problem_dir)
    ylim = (0,len(total))

    sentence_score = {}
    for n in range(N0,N):
        sentence_score[n] = Problem2Sentence().calc_score(sentence_dir, n)
        sentence_score[n] = map(clean_name, sentence_score[n])
    draw(sentence_score, "Sentence Extraction Score", ylim, "Number of predictions per label")

    word_score = {}
    for m in range(M0,M):
        word_score[m] = Sentence2Word().calc_score(word_dir, m)
        word_score[m] = map(clean_name, word_score[m])    
    draw(word_score, "Word Extraction Score", ylim, "Number of predictions per label")

    codeword_score = {}
    for p in range(P0,P):
        p_thresh = p
        codeword_score[p] = word2codeword.check_words(problem_dir, p_thresh)
        codeword_score[p] = map(clean_name, codeword_score[p])
    draw(codeword_score, "Codeword Translation Score", ylim, "Number of translations per word")

#     codeline_score1 = codeline_gen.check_sentences(problem_dir)
#     codeline_score1 = map(clean_name, codeline_score1)

    codeline_score2 = {}
    for q in range(Q0, Q):
        codeline_score2[q] = codeline_gen_dep.check_problems(problem_dir, q)
        codeline_score2[q] = map(clean_name, codeline_score2[q])
    draw(codeline_score2, "Codeline Building Score", ylim, "Number of wrong edges allowed")

#     print('wo dep: '+ str(set(problem_score).intersection(set(word_score)).intersection(set(codeword_score)).intersection(codeline_score1)))
    summary = ""
    if all_range and os.path.exists(intersections_path):
        shutil.rmtree(intersections_path)
    if not os.path.exists(intersections_path):
        os.mkdir(intersections_path)        
    summary += ' '.join(['{}: {}'.format(k, len(v)) for k, v in sentence_score.items()]) + '\n'
    summary += ' '.join(['{}: {}'.format(k, len(v)) for k, v in word_score.items()]) + '\n'
    summary += ' '.join(['{}: {}'.format(k, len(v)) for k, v in codeword_score.items()]) + '\n'
    summary += ' '.join(['{}: {}'.format(k, len(v)) for k, v in codeline_score2.items()]) + '\n'
    for n,m,p,q in product(range(N0,N),range(M0,M),range(P0,P), range(Q0,Q)):
        s = ""
        for fname in sorted(os.listdir(problem_dir)):
            if not fname.endswith('py'):
                continue
            fpath = os.path.join(problem_dir, fname)
            if not check_solution(fpath):
                continue  
            fname = clean_name(fname)
            base_pattern = "{:30} : {:10} {:10} {:10} {:10}\n"
            in_sentence = fname in sentence_score[n]
            in_word = fname in word_score[m]
            in_codeword = fname in codeword_score[p]
            in_codeline = fname in codeline_score2[q]
            s += base_pattern.format(fname, in_sentence, in_word, in_codeword, in_codeline)
#             s += base_pattern.format(fname, in_sentence, in_word, in_codeword)
        fname = 'intersection_{}_{}_{}_{}'.format(n,m,p,q)
        with open(os.path.join(intersections_path, fname), 'w') as f:
            f.write(s)
        result = (set(sentence_score[n])\
            .intersection(set(word_score[m]))\
            .intersection(set(codeword_score[p]))
            .intersection(set(codeline_score2[q])))
        summary += 'n:{} m:{} p:{} q:{} - {}\n'.format(n,m,p,q, len(result))
    if all_range:
        with open(os.path.join(intersections_path, 'summary'), 'w') as f:
            f.write(summary)
    show()
    
def main():
#     problem_dir = os.path.join('res', 'problems_test1')
    problem_dir = os.path.join('res', 'text&code8')
#     p_thresh = 0.5
    p = 1
    sentence_dir = os.path.join(problem_dir, 'sentence_json')
    n = 1
    word_dir = os.path.join(problem_dir, 'word_json')
    word_dir = os.path.join(problem_dir, 'word_test_json')
#     word_dir = os.path.join(problem_dir, 'word_json_struct')
#     word_dir = os.path.join(problem_dir, 'word_json_test_struct')
    m = 3

    intersections_path = os.path.join(problem_dir, 'intesections')
    N = M = P = 4
#     check_all_problems_intersection(sentence_dir, N, word_dir, M, problem_dir, P, intersections_path)
    
    tries = 10000
    solutions_dir = os.path.join(problem_dir, 'solutions')
    print(check_problems(problem_dir, sentence_dir, n, word_dir, m, p, tries, solutions_dir))
# ['AverageAverage.py', 'ChocolateBar.py', 'MarbleDecoration.py', 'SumOfPower.py']


    fname = 'CucumberMarket.py'
#     print(check_problem(fname, problem_dir, sentence_dir, n, word_dir, m, p, tries, solutions_dir))
#     fpath = os.path.join(solutions_dir, fname)
#     print(check_solution(fpath))
    
if __name__ == '__main__':
    main()