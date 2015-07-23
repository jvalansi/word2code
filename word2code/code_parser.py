'''
Created on Jan 20, 2015

@author: jordan
'''
import os
import re
import word_count
from problem_parser import parse_problem, compose_problem
import imp
import shutil
import ast
import parser
import astor
import copy
from ast import NodeTransformer, copy_location
from _ast import Name, Load
from solution_check import check_solution
# from problem2code import check_solution
# from problem2sentence import types

# transform: return len( set(way for way in ways if valid(way) ))
#
# return(len(set(foreach(height,ways,valid))))
#
# to:
#     value(return,len)
#     args(len,set)
#     args(set,ListComp)
#     elt(ListComp,way)
#     iter(ways,way)
#     ifs(way,valid)
#     args(valid,way)
#
#
# via:
# "Module(
#     body=[
#         Return(value=Call(
#             func=Name(id='len', ctx=Load()),
#             args=[Call(
#                 func=Name(id='set', ctx=Load()),
#                 args=[
#                     ListComp(elt=Call(
#                         func=Name(id='map', ctx=Load()),
#                         args=[Name(id='way', ctx=Load())],
#                         keywords=[], starargs=None, kwargs=None
#                     ),
#                     generators=[comprehension(
#                         target=Name(id='way', ctx=Store()),
#                         iter=Name(id='ways', ctx=Load()),
#                         ifs=[Call(
#                             func=Name(id='valid', ctx=Load()),
#                             args=[Name(id='way', ctx=Load())],
#                             keywords=[], starargs=None, kwargs=None
#                         )]
#                     )]
#                 )],
#                 keywords=[], starargs=None, kwargs=None
#             )], 
#             keywords=[], starargs=None, kwargs=None
#         ))
#     ]
# )"


def clean_code(code):
    '''
    clean code
    :param s: code string to clean
    '''
#     marks = r'\+\-=/\*\.,\''
#     code = re.sub('(['+marks+']+)', ' \\1 ', code)
    code = re.sub(r'\s+', ' ', code)
    code += '\n'
    return code

def count_code(path):
    '''
    count code words
    :param path:
    :return: word count of code
    '''
    code_data = ""
#     go through all files in directory
    for fname in os.listdir(path):
#         go through all lines in file
        with open(os.path.join(path, fname), 'r') as fobj:
            problem = fobj.read()
        problem_parse = parse_problem(problem)
        for sentence_parse in problem_parse['sentences']:
            for codeline in sentence_parse['code']:
#             else add to code data
                code_data += clean_code(codeline)
    word_counter = word_count.WordCount()
    word_counter.count_words(code_data, "res/code_data")
#     print(code_data)
    return(word_counter)

#     sentence: \s*\#({sentword} )*{sentword}
#     dependencies: \s*\#.+
#     definitions: 
#         \s*{sentword}\s+=\s+{code}
#         \s*def {sentword}({args}): return {code}
#         \s*{codeword}\s=\slambda\s{args}: {code}
#     code: ({sentword}(|\s|\sfor\s|\sin\s|,|)+
#     {args} -> {sentword\codeword}(, {sentword\codeword})*

#     # Return the least sum of two positive integers a and b such that P is a divisor of a* X +b* Y .
#     # ROOT-0(root=Return-1(dep=sum-4(det=the-2, amod=least-3, prep_of=integers-8(num=two-6, amod=positive-7)), rcmod=divisor-17(nsubj=a-9(conj_and=b-11, dep=such-12, prep_that=P-14), cop=is-15, det=a-16, prep_of=X-21(det=a-19, nn=*-20, conj_+=b-23), dep=Y-25(dep=*-24))))
#     least = min
#     def divisor(x,y): return mod(y,x)==0
#     return(least(sum((a,b)) for a,b in product(range(1,P),repeat=2) if divisor(P,a* X +b* Y)))

#     insert = lambda possibility: A[:possibility] + B + A[possibility:]
    
#     sentence: \s*\#({sentword} )*{sentword}
#     #### {codeline_type} = ({sentword}(|\s|\sfor\s|\sin\s|,|)+
#     {codeline_type} = ({codeword}(|\s|\sfor\s|\sin\s|,|)+
#     #### return(reduce(map(mapping, filter( valid, possibilities)))) 
#     return(reduce(map(mapping, filter(valid, possibilities)))) 

#     # Your method should return the maximum number of consecutive competitions with positive rating changes.
#     #### possibilities = consecutive(competitions)
#     possibilities = csubsets(input_array)
#     #### mapping = lambda possibility: number(possibility)
#     mapping = lambda possibility: len(possibility)
#     #### valid = lambda competitions: all(map(positive ,competitions))
#     valid = lambda possibility: all(map(is_positive, possibility))
#     #### reduce = lambda possibility: maximum(possibility)
#     reduce = lambda possibility: max(possibility)
#     #### return(reduce(map(mapping, filter( valid, possibilities)))) 
#     return(reduce(map(mapping, filter(valid, possibilities)))) 

class DelGen(NodeTransformer):
    def __init__(self, args):
        self.args = args
        
    def visit_GeneratorExp(self, node):
        return copy_location(self.args, node)

def find_node_type(node, node_type):
    walk = ast.walk(node)
    for w in walk:
        if type(w).__name__ == node_type:
            return copy.deepcopy(w)

def gen_codeline_type(codeline):
    new_code = []
    parse = ast.parse(codeline.strip())
    return_parse = find_node_type(parse, 'Return')
    if not return_parse:
        return [codeline]
#     print(astor.dump(parse))
    reduce_parse = return_parse.value
    generator_parse = find_node_type(reduce_parse, 'GeneratorExp')
    if not generator_parse:
        new_code.append('reduce = lambda possibility: '+astor.to_source(reduce_parse))
        new_code.append('return(reduce(possibilities))')
        return ['return ' + astor.to_source(reduce_parse)]
    args = Name(id='possibility', ctx=Load())
    dg = DelGen(args)
    dg.visit(reduce_parse)
    new_code.append('reduce = lambda possibility: '+astor.to_source(reduce_parse))
#         print(astor.to_source(reduce_parse))
    target = generator_parse.generators[0].target
    mapping_parse = generator_parse.elt
    new_code.append('mapping = lambda '+astor.to_source(target)+': '+astor.to_source(mapping_parse))
#             print(astor.to_source(mapping_parse))
    possibilities_parse = generator_parse.generators[0].iter
    new_code.append('possibilities = ' + astor.to_source(possibilities_parse))
#             print(astor.to_source(possibilities_parse))
    valid_parse = None
    if generator_parse.generators[0].ifs:
        valid_parse = generator_parse.generators[0].ifs[0]
        new_code.append('valid = lambda '+astor.to_source(target)+': '+astor.to_source(valid_parse))
#                 print(astor.to_source(valid_parse))
    if valid_parse:
        new_code.append('return(reduce(map(mapping, filter(valid, possibilities))))')
    else:
        new_code.append('return(reduce(map(mapping, possibilities)))')
    return new_code

def to_codeline_type(sentence_parse):
    '''
    transform:
        #### def valid(k):  return same(contain(cows, part) for part in parts(k))
        def valid(k):  return same(contain(cows, part) for part in parts(k))
    to:
        def valid(possibility):
            #### def mapping(possibility): return contain(part, cows)
            def mapping(possibility): return countOf(possibility, cows)
            #### def parts(k): return str[:k], str[k:]
            def possibilities(possibility): return str[:k], str[k:]
            #### def reduce(possibility): return same(*possibility)
            def reduce(possibility): return eq(*possibility)
            #### return(reduce(map(mapping(possibilities(possibility))))
            return(reduce(map(mapping(possibilities(possibility))))
    
    :param sentence_parse:
    '''
    print(sentence_parse['code'])
    if not sentence_parse['code']:
        return
    codeline = sentence_parse['code'].pop()
    translation = sentence_parse['translations'].pop() if sentence_parse['translations'] else copy.deepcopy(codeline)
    try: 
        parse = ast.parse(codeline.strip())
    except Exception:
        return
#     print(astor.dump(parse))
    tc= TranslateCode({})
    if parse.body and type(parse.body[0]).__name__ == 'FunctionDef':
        method_parse = copy.deepcopy(parse)
#         print(astor.dump(method_parse))
        args_parse = method_parse.body[0].args.args 
        if args_parse and hasattr(args_parse[0], 'id'):
            args_name = args_parse[0].id
            transdict = {args_name : 'possibilities'}
            tc.transdict = transdict
#             tc.visit(method_parse)
        del method_parse.body[0].body[0]
        sentence_parse['method'] = [astor.to_source(method_parse)]
    sentence_parse['translations'].extend(gen_codeline_type(translation))
#     tc.visit(parse)
    codeline = astor.to_source(parse)
    sentence_parse['code'].extend(gen_codeline_type(codeline))

class TranslateCode(NodeTransformer):
    def __init__(self, transdict={}, translate=True):
        self.transdict = transdict
        self.translate = translate

#     def visit_FunctionDef(self, node):
#         self.generic_visit(node)
# #         print(astor.dump(node))
#         target_parse = node.name
#         if target_parse in types:
#             return node
#         self.gendict[target_parse] = Name(id='mapping')
#         new_node = copy.deepcopy(node)
#         new_node.name = 'mapping'
#         return copy_location(new_node, node)

    def visit_Assign(self, node):
        if type(node.value).__name__ in ['Name', 'Num']:
            target_parse = node.targets[0]
            if type(node.value).__name__ == 'Name':
                value_parse = node.value.id
            elif type(node.value).__name__ == 'Num':
                value_parse = node.value.n
#             value_parse =  node.value
            self.transdict[target_parse.id] = value_parse
            return
        self.generic_visit(node)
        return node


    def visit_Name(self, node):
        self.generic_visit(node)
        if not self.translate:
            return node 
        if node.id in self.transdict:
            v = self.transdict[node.id]
            node.id = v
            return node
        return node

class GeneralizeCode(NodeTransformer):
    def __init__(self, gendict={}):
        self.gendict = gendict

#     def visit_Assign(self, node):
#         self.generic_visit(node)
#         if type(node.value).__name__ == 'Call':
#             target_parse = node.targets[0]
#             self.gendict[target_parse.id] = 'possibilities'
#             target_parse.id = 'possibilities'
#             return node
#         return node

    def visit_Call(self, node):
        self.generic_visit(node)
#         print(astor.dump(node))
        if hasattr(node.func, 'id') and node.func.id == 'filter':
            self.gendict[node.args[0].id] = 'valid'
            node.args[0].id = 'valid'
            if hasattr(node.args[1], 'id'):
                self.gendict[node.args[1].id] = 'possibilities'
                node.args[1].id = 'possibilities'
        if hasattr(node.func, 'id') and node.func.id == 'map':
            self.gendict[node.args[0].id] = 'mapping'
            node.args[0].id = 'mapping'
            if hasattr(node.args[1], 'id'):
                self.gendict[node.args[1].id] = 'possibilities'
                node.args[1].id = 'possibilities'
        return node

    def visit_FunctionDef(self, node):
        self.generic_visit(node)
#         print(astor.dump(node))
        if node.name in self.gendict:
            node.name = self.gendict[node.name]
        return node

    def visit_Name(self, node):
        self.generic_visit(node)
        if node.id in self.gendict:
            node.id = self.gendict[node.id]
            return node
        return node


def to_single_line(sentence_parse):
    '''
    compress multiline code to single line
    
    :param sentence_parse: sentence_parse to compress to single line
    '''
    code = sentence_parse['code']
#     print(code)
    if len(code) <= 1:
        return
    new_code = []
    new_translations = []
    transdict = {}
#     for codeline in code[:-1]:
#     for codeline in code:
#         parse = ast.parse(codeline.strip())
#         if type(parse.body[0]).__name__ == 'Assign' and type(parse.body[0].value).__name__ in ['Name', 'Str', 'Num']:
#             target_parse = parse.body[0].targets[0]
#             value_parse =  parse.body[0].value
#             transdict[astor.to_source(target_parse)] = value_parse
#         else:
#             new_translations.append(codeline.strip())
#             tc = TranslateCode(transdict)
#             tc.visit(parse)
#             new_code.append(re.sub('\s+',' ',astor.to_source(parse)))
    parse = ast.parse('\n'.join([codeline.strip() for codeline in code]))
    translation_parse = copy.deepcopy(parse)
    TranslateCode(transdict, False).visit(translation_parse)
    TranslateCode(transdict).visit(parse)
#     new_code.append(re.sub('\s+',' ',astor.to_source(parse)))
    new_code.append(clean_code(astor.to_source(parse)))
    new_translations.append(clean_code(astor.to_source(translation_parse)))
    sentence_parse['code'] = new_code
    sentence_parse['translations'] = new_translations
#     print('code: '+str(sentence_parse['code']))
#     print('translations: '+str(sentence_parse['translations']))
    return


def lambda2def(code):
#     valid = lambda possibility: exactly(k, len(changed(message,possibility)))
#     ->
#     def valid(possibility): return exactly(k, len(changed(message,possibility)))
    new_code = []
    for codeline in code:
        lambda_pattern = r'(?P<indent>\s*)(?P<func>\S+)\s*=\s*(?P<parentheses>\()?lambda\s+(?P<args>[^:]+)\s*:\s*(?P<content>.+)(?(parentheses)\))' 
        m = re.match(lambda_pattern, codeline)
        if m:
            d = m.groupdict()
            new_code.append('{indent}def {func}({args}): return {content}'.format(**d))
        else:
            new_code.append(codeline)
    return new_code

def to_quotation_mark(problem):
    problem_parse = parse_problem(problem)
    for sentence_parse in problem_parse['sentences']:
        sentence_parse
    
def to_generic_names(problem_parse):
    d = {}
    for sentence_parse in reversed(problem_parse['sentences']):
        method_parse = sentence_parse['method'][0]
        if method_parse:
            method_ast = ast.parse(method_parse.strip()+' pass')
#             print(astor.dump(method_ast))
            gc = GeneralizeCode(d)
            gc.visit(method_ast)
            d = gc.gendict
            new_method = re.sub('pass', '', astor.to_source(method_ast))
            sentence_parse['method'][0] = new_method
        new_code = []
        for codeline in sentence_parse['code']:
            codeline_ast = ast.parse(codeline.strip())
#             print(astor.dump(codeline_ast))
            gc = GeneralizeCode(d)
            gc.visit(codeline_ast)
            d = gc.gendict
            new_code.append(clean_code(astor.to_source(codeline_ast)))
        sentence_parse['code'] = new_code
    return problem_parse

def parse_problem_code(fname, in_path, out_path):
    fpath = os.path.join(in_path, fname)
    with open(fpath) as f:
        problem = f.read()
    problem_parse = parse_problem(problem)
    for sentence_parse in problem_parse['sentences']:
        if re.search(r'ROOT-0', sentence_parse['sentence']):
            print(sentence_parse['sentence'])
            sentence_parse['sentence'] = ''
        code = sentence_parse['code']
        code = lambda2def(code)
#         code = to_single_line(code)
        sentence_parse['code'] = code
        to_single_line(sentence_parse)
        to_codeline_type(sentence_parse)
    problem_parse = to_generic_names(problem_parse)
    print(problem_parse['sentences'])
    problem = compose_problem(problem_parse)
    out_fpath = os.path.join(out_path, fname) 
    with open(out_fpath, 'w') as f:
        f.write(problem)
    return problem

def is_empty(problem):
    problem_parse = parse_problem(problem)
    for sentence_parse in problem_parse['sentences']:
        if sentence_parse['code'] and not re.match('^\s*pass\s*$', sentence_parse['code'][0]):
            print(sentence_parse['code'])
            return False
    return True

def parse_problems_code(path, out_path):
    success = []
#     not_empty = []
    if os.path.exists(out_path):
        shutil.rmtree(out_path)
    os.mkdir(out_path)
    for fname in sorted(os.listdir(path)):
        if not fname.endswith('.py'):
            continue
        print(fname)
        fpath = os.path.join(path, fname)
        if not check_solution(fpath):
#             not_empty.append(fname)
            continue
        parse_problem_code(fname, path, out_path)
        out_fpath = os.path.join(out_path, fname)
        if check_solution(fpath) and not check_solution(out_fpath):
            success.append(fname)
    return success

if __name__ == '__main__':
#     print(count_code('res/text&code5/'))

#     code = ''' 
#         least = min
#         def divisor(x,y): return mod(y,x)==0
#         return(least(sum((a,b)) for a,b in product(range(1,P),repeat=2) if divisor(P,a* X +b* Y)))
#     '''
#     print(add_translation(code))
    
    path = 'res/translations'
    out_path = 'res/translations1'
    print(parse_problems_code(path, out_path))
    fname = 'CorruptedMessage.py'
#     fname = 'RaiseThisBarn.py'
#     fname = 'SumOfPower.py'
#     fname = 'DecipherabilityEasy.py'
#     fname = 'PalindromesCount.py'
#     fname = 'InfiniteString.py'
#     fname = 'TextStatistics.py'    
#     parse_problem_code(fname, path, out_path)


#TODO: fix reduce only sentences