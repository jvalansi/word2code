'''
Created on Jan 20, 2015

@author: jordan
'''
import os
import re
import word_count

# transform: return len( set(way for way in ways if valid(way) ))
#
# return(len(set(foreach(height,ways,valid))))
#
# to:
#     args(return,len)
#     args(len,set)
#     args(set, ways)
#     elt(ways,way)
#     map(way,way)
#     ifs(way,valid)
#
#     value(return,len)
#     args(len,set)
#     args(set,ListComp)
#     elt(ListComp,way)
#     iter(ways,way)
#     ifs(way,valid)
#     args(valid,way)
#
#     value(return,len)
#     args(len,set)
#     args(set,ListComp)
#
#     value(return,len)
#     args(len,set)
#     args(set,ListComp)
#     elt(ListComp,map)
#     args(map,way)
#     gen
#
# via:
# "Module(
#     body=[
#         Return(
#             value=Call(
#                 func=Name(id='len', ctx=Load()),
#                 args=[
#                     Call(
#                         func=Name(id='set', ctx=Load()),
#                         args=[
#                             ListComp(
#                                 elt=Call(
#                                     func=Name(id='map', ctx=Load()),
#                                     args=[Name(id='way', ctx=Load())],
#                                     keywords=[],
#                                     starargs=None,
#                                     kwargs=None
#                                 ),
#                                 generators=[
#                                     comprehension(
#                                         target=Name(id='way', ctx=Store()),
#                                         iter=Name(id='ways', ctx=Load()),
#                                         ifs=[
#                                             Call(
#                                                 func=Name(id='valid', ctx=Load()),
#                                                 args=[Name(id='way', ctx=Load())],
#                                                 keywords=[],
#                                                 starargs=None,
#                                                 kwargs=None
#                                             )
#                                         ]
#                                     )
#                                 ]
#                             )
#                         ],
#                         keywords=[],
#                         starargs=None,
#                         kwargs=None
#                     )
#                 ],
#                 keywords=[],
#                 starargs=None,
#                 kwargs=None
#             )
#         )
#     ]
# )"


def clean_code(code):
    '''
    clean code
    :param s: code string to clean
    '''
    marks = r'\+\-=/\*\.,\''
    code = re.sub('(['+marks+']+)', ' \\1 ', code)
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
            lines = fobj.readlines()
        for line in lines:
#             stop when reaching main
            if re.search("if __name__ == '__main__':", line):
                break
#            if comment (starts with '#') continue
            if re.search(r'^(\s+)?#.*', line) or \
                re.search(r"class\s.+:", line) or \
                re.search(r"def\s.+:", line) or \
                re.search(r'input_array\d?\s=', line) or\
                re.search(r'input_int\d?\s=', line):
                continue
            if not re.search(r'valid\s*=', line):
                continue
#             else add to code data
            code_data += clean_code(line)
    word_counter = word_count.WordCount()
    word_counter.count_words(code_data, "code_data")
    print(code_data)

if __name__ == '__main__':
    count_code('res/text&code2/')
