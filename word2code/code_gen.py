'''
Created on Jan 31, 2015

@author: jordan
'''
import os
import re
import TopCoderSpider
import itertools
from utils import *
import pickle
from problem import Problem 
import sys

#       generate possibilities statement
possibilities = ['subsets', 'csubsets']
#       generate valid statement
valids = ['all', 'any', 'not all', 'not any']
        
relations = ['==','>=','>','<','<=','!=']
#       generate mapping statement
mappings = ['']
#       generate return statement
reduces = ['','min','max','len', 'sum', 'average']

#     generate code
def solve(input_string, possible_solution): 

#         solution = \
    input_array = eval(input_string)
    N = len(input_array)
    possibilities = eval("{}(input_array)".format(possible_solution[0]))
    mapping = lambda possibility: eval("{}(possibility)".format(possible_solution[1]))
    valid = lambda possibility: eval("{}(pair[0] {} pair[1] for pair in {}(possibility , 2))".format(possible_solution[2],possible_solution[3],possible_solution[4]))
    return_statement = "{}([mapping(possibility) for possibility in possibilities if valid(possibility)])".format(possible_solution[5])
#         print(return_statement) 
    return(eval(return_statement))
#         """.format(input_string = input_string, 
#                    possibility1 = ,
#                    mapping = possible_solution[1],
#                    valid = possible_solution[2],
#                    relation = possible_solution[3],
#                    possibility2 = possible_solution[4],
#                    reduce = possible_solution[5])
#         print(solution)
        
#     check code against input and output
def get_examples(examples_dir):
    print('getting examples')
    simple_examples = []
    for fname in os.listdir(examples_dir):
        if not fname.endswith('.pkl'):
            continue
        print(fname)
        problem = pickle.load(open(examples_dir+fname,'r'))
        examples = problem.examples
        print(len(examples))
        simple_examples.append(examples)
#         simple_examples.append(examples[:1])
    return simple_examples
        
def parse_examples(examples):
    parsed = []
    for example in examples:
        input_string = parse_string(example['inputs'][0])
        print('len: '+str(len(input_string)))
        if len(input_string) >= 15:
            return parsed
        print('example input: '+input_string)
        output_string = parse_string(example['output'])
        print('example output: '+output_string)
        parsed.append((input_string,output_string))
    return parsed

def check_outputs(examples,possible_outputs):
    return all(examples[i][1] == str(possible_outputs[i]) for i in range(len(examples)))

def check_code(code_dir):
    examples_list = get_examples(code_dir)
    print('solving')
    success = 0
    tried = 0
    for examples in examples_list:
        examples = parse_examples(examples)       
        if not examples:
            continue
        tried += 1
        possible_solutions = itertools.product(possibilities,reduces,valids,relations,possibilities,reduces)
        for possible_solution in possible_solutions:
#             print(possible_solution)
            try:
                possible_outputs = []
                for (input_string, output_string) in examples:
                    possible_outputs.append(solve(input_string, possible_solution))
#                 print(possible_output0)
#                 print(possible_output1)
                if check_outputs(examples,possible_outputs):
                    print('success')
                    success += 1
                    break
#             except TypeError:
#                 print('type error')
#             except ValueError:
#                 print('value error')
#             except ZeroDivisionError:
#                 print('zero division error')
            except Exception:
                continue
    print(tried) 
    print(success)
        
def parse_string(s):
    s = re.sub('{','[',s)
    s = re.sub('}',']',s)     
    s = re.sub('\n',' ',s)
    return s   

if __name__ == '__main__':
    main_code_dir = 'res/brute_force_easy/'
    check_code(main_code_dir)