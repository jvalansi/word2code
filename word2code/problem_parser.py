'''
Created on Apr 6, 2015

@author: jordan
'''
import re
import os
import shutil
import json
from nltk.tokenize import sent_tokenize
from stanford_corenlp import sentence2dependencies
from solution_check import check_solution
from dependency_parser import Node

# from utils import *
# from operator import *
#
# class AlienAndPassword:
#     # Alien Fred wants to destroy the Earth, but he forgot the password that activates the planet destroyer.
#
#     # You are given a String S.
#     def getNumber(self, S):
#         input_array = numpy.array(list(S))
#         N = input_array.shape
#         possibilities = subsets(input_array)
#
#     # Fred remembers that the correct password can be obtained from S by erasing exactly one character.
#
#     # the correct array can be done from S by removing exactly 1 element
#     ####    correct = lambda array: exactly(len(removing(S, array)), 1)
#         valid = lambda possibility: eq(len(diff(input_array, possibility)), 1)
#
#     # Return the number of different passwords Fred needs to try.
#     ####    return(number(different(possibility for possibility in passwords if valid(possibility))))
#         return(len(set(possibility for possibility in possibilities if valid(possibility))))
#
#
# if __name__ == '__main__':
#     S = 'aa'
#     aap = AlienAndPassword()
#     print(aap.getNumber(S))
#         \s*(?P<vars>[^#]+\n)*
#         \s*(?P<sentences>(?:.*\n)+)
#         \s*(?P<example>def\s+example\d+\(\):\s*\n(?:[^\n]*\w[^\n]+\n)+)+
#         \s*(?P<main>if\s+__name__\s*==\s*\'__main__\'\s*:\s*\n.*)
def parse_problem(problem):
    parse = {}
    problem_pattern = re.compile(r'''
        \s*(?P<imports>(?:.*\bimport\b.*\n)+)?\s*
        \s*(?P<class>class\s+.+:)\s*
        \s*(?P<method>def\s+.+\(self(?:\s*,\s*.+)*\):)\s*
        \s*(?P<vars>(?:[^\#]+\n)+)?\s*
        \s*(?P<sentences>(.*\n)+?)\s*
        \s*
        \s*(?P<example>(?:def\s+example\d+\(\):\s*\n(?:[^\n]*\w[^\n]+\n)+\s*)+)\s*
        \s*(?P<main>\s*if\s+\(?__name__\s*==\s*\'__main__\'\)?\s*:\s*\n.*)\s*
        ''', re.VERBOSE | re.MULTILINE)
    m = problem_pattern.match(problem)
    parse = m.groupdict()
    parse['sentences'] = parse_content(parse['sentences'])
#     parse = {}
#     import_pattern = r'\s*import\s+\S+|from\s+.+\s+import\s+.+\s*'
#     parse['import'] = re.findall(import_pattern,problem)
#     class_pattern = r'\s*class\s+.+:\s*'
#     parse['class'] = re.findall(class_pattern,problem)
#     class_method_pattern = r'\s*(def\s+.+\(self(?:\s*,\s*.+)*\):)\s*\n(?:[^#]+\n)*'
#     parse['method'] = re.findall(class_method_pattern,problem)
#     class_vars_pattern = r'\s*def\s+.+\(self(?:\s*,\s*.+)*\):\s*\n(?:([^#]+)\n)*'
#     parse['vars'] = re.findall(class_vars_pattern,problem)
#     example_pattern = r'\s*def\s+example\d+\(\):\s*\n(?:[^\n]*\w[^\n]+\n)+'
#     parse['example'] = re.findall(example_pattern, problem)
#     main_pattern = r'\s*if\s+\(?__name__\s*==\s*\'__main__\'\)?\s*:\s*\n.*'
#     parse['main'] = re.findall(main_pattern,problem)
#     sentence_method_pattern = r'\s*def\s+.+\([^\)]*\):\s\n*'
#     code_pattern = r'[^#\n]*\w[^#\n]+\n'
#     sentences_pattern = r'(?:\s*#[^#].+\n)(?:'+sentence_method_pattern+r'\n)?(?:\s*####.+\n.+\n)*(?:'+code_pattern+')*'
# #     sentences_pattern = '(?:[ \t\r\f\v]*#[^#].+\n)+'
#     sentences = re.findall(sentences_pattern,problem)
#     parse['sentences'] = [parse_sentence(sentence) for sentence in sentences]
    return parse

def parse_content(content):
    sentences = []
    sentence_pattern = re.compile(r"""
        \s*\#[^\#\n].+\n
        (?:\s*def\s+.+\(.*\):)?
        (?:\s*\#\#\#\#.+\n.+\n)*
        (?:[^\#\n]+\n)*
    """, re.VERBOSE|re.MULTILINE)
    matches = sentence_pattern.findall(content)
    for m in matches:
        sentences.append(parse_sentence(m))
    return sentences

def parse_sentence(sentence):
    parse = {}
    sentence_method_pattern = r'\s*def\s+.+\(.*\):\s*'
    code_pattern = r'^[^#\n]*\w[^#\n]+\n'
    comment_pattern = r'(\s*#[^#].+\n)(?:'+sentence_method_pattern+r'\n)?(?:\s*####.+\n.+\n)*(?:'+ code_pattern +r')*'
    comments = re.findall(comment_pattern, sentence, re.MULTILINE)
    parse['sentence'] = ' '.join([re.sub(r'^\s*#','',comment) for comment in comments])
    method_pattern = r'(?:\s*#[^#].+\n)('+sentence_method_pattern+r'\n)?(?:\s*####.+\n.+\n)*(?:'+ code_pattern +r')*'
    parse['method'] = re.findall(method_pattern, sentence, re.MULTILINE)
    translation_pattern = r'(?:\s*####(.+\n).+\n)'
    parse['translations'] = re.findall(translation_pattern, sentence, re.MULTILINE)
#     codeline_pattern = r'(?:\s*####.+\n(.+\n))'
    codeline_pattern = r'[\#\n]+\n'
    parse['code'] = re.findall(codeline_pattern, sentence, re.MULTILINE)
#     extra_code_pattern = r'(?:\s*#[^#].+\n)(?:'+sentence_method_pattern+r'\n)?(?:\s*####.+\n.+\n)*('+ code_pattern +r')*'
    extra_code_pattern = code_pattern 
    extra_code = re.findall(extra_code_pattern, sentence, re.MULTILINE)
    for codeline in extra_code:
        if codeline in parse['code'] or codeline in parse['method']:
            continue
        parse['code'].append(codeline)
    return parse

def parse_dir(problem_dir):
    parses = []
    for fname in os.listdir(problem_dir):
        with open(fname,'r') as f:
            problem = f.read()
            parses.append(parse_problem(problem))
    return parses

def print_deps(parse):
    deps = sentence2dependencies(parse['sentence'])[0]
#     sentence += '\n'.join([indenter*indent+'# '+str(dep) for dep in deps]) +'\n'
    root = Node('ROOT-0')
#     deps = codeline_gen_dep.clean_dependencies(deps)
    return str(root.deps2tree(deps))


def compose_sentence(parse):
    sentence = ''
    sentence += indenter*2 + '# ' + parse['sentence'].strip() + '\n'
#     sentence += indenter*2 + '\' ' + parse['sentence'].strip() + '\'\n'
    if not parse['code']:
        return sentence
    method = parse['method'][0]
    if method:
        sentence += indenter*2 + method.strip() + '\n'
    indent = 2 + bool(method)
    for i,codeline in enumerate(parse['code']):
        if i in range(len(parse['translations'])):
            translation = parse['translations'][i]
            sentence += indenter*indent + '#### ' + translation.strip() + '\n'
        sentence += indenter*indent + codeline.strip() + '\n'
#     sentence += indenter*indent+'# '+ print_deps(parse) + '\n'
    return sentence

indenter = ' '*4

def compose_problem(parse):
    problem = ''
    if parse['imports']:
        problem += parse['imports'] +'\n'
    problem += '\n'
    problem += parse['class'].strip() + '\n'
    problem += indenter + parse['method'].strip() + '\n'
    if parse['vars']:
        for var_parse in parse['vars'].split('\n'):
            problem += indenter*2 + var_parse.strip() + '\n'
    for sentence_parse in parse['sentences']:
        problem += compose_sentence(sentence_parse)
    problem += '\n'
    problem += parse['example']
    problem += parse['main']
    return problem

def json2method(definiton_json):
    method = ''
# String[] draw(int xCount)
    m = re.match(r'.+\s\w+\((?P<args>.+)\)',definiton_json['method_signature'])
    args = re.split(', ', m.group('args'))
    inputs = []
    input_arrays = []
    input_ints = []
    for arg in args:
        arg_type,arg_name = arg.split(' ')
        inputs.append(arg_name)
        if arg_type == 'int':
            input_ints.append(arg_name)
        else:
            input_arrays.append(arg_name)
    method += '\tdef {}(self, {}):\n'.format(definiton_json['method_name'], ', '.join(inputs))
    if len(input_arrays)==1:
        method += '\t\tinput_array = {}\n'.format(input_arrays[0])
    else:
        for i,arg_name in enumerate(input_arrays):
            method += '\t\tinput_array{} = {}\n'.format(i,arg_name)
    if len(input_ints)==1:
        method += '\t\tinput_int = {}\n'.format(input_ints[0])
    else:
        for i,arg_name in enumerate(input_ints):
            method += '\t\tinput_int{} = {}\n'.format(i,arg_name)
    return method

def json2var(var_json):
    var = var_json
#     var = re.sub('\n+','\n', var)
    var = re.sub(r'\s+',' ', var)
    var = re.sub(r'\{','[', var)
    var = re.sub(r'\}',']', var)
    return var

def json2problem(problem_json):
    problem = ''
    problem += 'from utils import *\n\n'
    problem += 'class {}:\n'.format(problem_json['Definition']['class_name'])
    problem += json2method(problem_json['Definition'])
    problem_statement = re.sub(r'\s+', ' ', problem_json['Problem Statement'])
    for sent in sent_tokenize(problem_statement):
        for s in sent.split('\n'):
            problem += '\t\t# {}\n'.format(s)
    problem += '\t\tpass\n\n'
    for i,example in enumerate(problem_json['Examples']):
        problem += 'def example{}():\n'.format(i)
        problem += '\tcls = {}()\n'.format(problem_json['Definition']['class_name'])
        for j,input_json in enumerate(example['inputs']):
            problem += '\tinput{} = {}\n'.format(j,json2var(input_json))
        problem += '\treturns = {}\n'.format(json2var(example['output']))
        problem_vars = ', '.join(['input{}'.format(j) for j in range(len(example['inputs']))])
        problem += '\tresult = cls.{}({})\n'.format(problem_json['Definition']['method_name'], problem_vars)
        problem += '\treturn result == returns\n\n'
    problem += "if __name__ == '__main__':\n\tprint(example0())\n\n"
    return problem

def json2problem_dir(indir, outdir):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    for fname in sorted(os.listdir(indir)):
        fbase, fext = os.path.splitext(fname)
        if fext != '.json':
            continue
        print(fname)
        with open(os.path.join(indir,fname)) as fp:
            problem_json = json.load(fp)
        fbase = problem_json['Definition']['class_name']
        with open(os.path.join(outdir, fbase+'.py'), 'w') as fp:
            fp.write(json2problem(problem_json))

if __name__ == '__main__':
#     with open('res/translations/CorruptedMessage.py') as f:
#         problem = f.read()
#     parse = parse_problem(problem)
#     print(parse)
# #     with open('res/parse', 'w') as f:
# #         json.dump(parse,f,indent=4, separators=(',', ': '))
#     with open('res/compose.py', 'w') as f:
#         f.write(compose_problem(parse))

#     indir = 'res/brute_force_easy/'
#     outdir = 'res/problems_test/'
#     json2problem_dir(indir, outdir)

#     root = codeline_gen_dep.Node('ROOT-0')
#     sentence = 'hello, how are you'
#     deps = sentence2dependencies(sentence)[0]
#     deps = codeline_gen_dep.clean_dependencies(deps)
#     print(deps)
#     print(root.deps2tree(deps))


    indir = 'res/text&code6/'
    outdir = 'res/test/'
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    os.mkdir(outdir)
    for fname in sorted(os.listdir(indir)):
        fbase, fext = os.path.splitext(fname)
        if fext != '.py':
            continue
        if not check_solution(os.path.join(indir, fname)):
            continue
#         print(fname)
        with open(os.path.join(indir,fname)) as fp:
            problem = fp.read()
        parse = parse_problem(problem)
        with open(os.path.join(outdir, fname), 'w') as fp:
            fp.write(compose_problem(parse))
        if not check_solution(os.path.join(outdir, fname)):
            print(fname)
