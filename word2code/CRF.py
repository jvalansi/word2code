'''
Created on Feb 12, 2015

@author: jordan
'''
import nltk
import subprocess
import re
import numpy
from collections import Counter
import json
import string
import os
import copy
import shutil

labels = ['', 'N-', 'in',   'if', ' ',  'for',    'valid',
 '=',  'N+', 'return', 'string', 'mapping',  'else',
   'lambda']
array = ['input_array','possibilities','elements','possibility',]
primitive = ['j', 'i', 'inf', 'N','element','number','input_int', ]
possibilities = ['csubset','range', 'subsets', ]
unary_operator = ['abs', 'int','str','tuple','inclusive', ]
binary_operator = ['sub', 'mod','add',   '-',]
array_operator = ['countOf',  'itemgetter', 'indexOf', ]
array2array_operator = ['delete','diff', 'where','set','sorted',]
comparison = ['gt','eq', 'neq', '>', 'leq', ]
unary_logic = ['not',  ]
binary_logic = ['and','or', ]
array_logic = ['all','any',]
valid = ['contains','is_prime','successive', ]
reduce = ['min', 'sum','len','max','average', ]

non_labels = ['(',',',')','[',']', ':', '.']





def join_files(files_dir, fnames):
    with open('res/train', 'w') as outfile:
        for fname in fnames:
            with open(os.path.join(files_dir,fname)) as infile:
                for line in infile:
                    outfile.write(line)
                outfile.write('\n\n')

def test(train_dir, output_dir, test_dir=None, features=2):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)
    if not test_dir:
        test_dir = train_dir
    test_fnames = sorted(os.listdir(test_dir))
    train_fnames = sorted(os.listdir(train_dir))
    for index,fname in enumerate(test_fnames):
        print(fname)
        train_fnames_ = copy.copy(train_fnames)
        if fname in train_fnames:
            train_fnames_.remove(fname)
        join_files(train_dir, train_fnames_)
        cmd = '/home/jordan/Downloads/CRF++-0.58/crf_learn res/features{} res/train res/model'.format(features)
        output = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
        cmd = '/home/jordan/Downloads/CRF++-0.58/crf_test -v2 -m res/model {}'.format(os.path.join(test_dir,fname))
        output = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
        sentences_json = output2json(output)
        json_file = os.path.join(output_dir,fname)
        with open(json_file, 'w') as outputjson:
            json.dump(sentences_json, outputjson, indent = 4, separators=(',', ': '))
#         with open(os.path.join(output_dir,fname),'w') as outputfile:
#             outputfile.write(output)
# #             outputfile.write('----------------------\n')


prediction_pattern = r'\w+/\d\.\d+'
line_pattern = r'(?:\S+)\s+(?:\w+\s+)+(?:\w+)\s+(?:'+prediction_pattern+r'\s+)+'
# named_line_pattern = r'(:P<word>\S+)\s+(:P<features>(?:\S+\s+)+)(:P<label>\w+)\s+(:P<predictions>(?:'+prediction_pattern+r'\s+)+)'
# named_line_pattern = r'(:P<word>\S+)\s+(?:\w+\s+)+(:P<label>\w+)\s+(?:'+prediction_pattern+r'\s+)+'
named_line_pattern = r'(?P<line>(?P<word>\S+)\s+(?P<features>(?:\S+\s+)+)(?P<label>\w+)\s+(?P<prediction>'+prediction_pattern+')(?P<probs>(?:\s+'+prediction_pattern+r')+))'
sentence_pattern = r'#\s+\d\.\d+\n(?P<lines>(?:'+named_line_pattern+r')+)'

def output2json(output):
    sentences_json = []
#         sentences = re.findall(sentence_pattern, problem)
    sentences = re.split('\n\n+\#\s+\d\.\d+\n', output)
    for sentence in sentences:
        lines_json = []
        lines = re.split('\n', sentence)
        for line in lines:
            m = re.match(named_line_pattern, line)
            if not m:
                continue
            d = m.groupdict()
            d['features'] = d['features'].split()
            d['probs'] = str([(prediction.split('/')[1], prediction.split('/')[0]) for prediction in d['probs'].split()])
            d['prediction'] = (d['prediction'].split('/')[1], d['prediction'].split('/')[0])
#             word,pos,feature,label = line.split()[:4]
#             predictions = re.findall(prediction_pattern, line)
#             predictions = [(prediction.split('/')[1], prediction.split('/')[0]) for prediction in predictions]
#             prediction = predictions[0]
#             probs = predictions[1:]
#             probs = sorted(probs, reverse = True)
#             d = {'word':word, 'pos':pos, 'feature':feature, 'label':label, 'prediction':prediction, 'probs':str(probs)}
#                 lines_json.append(' '.join([word,pos,label,str(prediction),str(probs)]))
            lines_json.append(d)
        sentences_json.append(lines_json)
#         problems_json.append(sentences_json)
    return sentences_json

def output2json_dir(output_dir,json_dir):
    if not os.path.exists(json_dir):
        os.mkdir(json_dir)

#     problems_json = []
#     with open(output_dir,'r') as outputfile:
#         output = outputfile.read()
#     problem_pattern = '(?:'+sentence_pattern+')+-+\n'
#     problems = re.findall(problem_pattern, output)
#     for problem in problems:
    fnames = sorted(os.listdir(output_dir))
    for fname in fnames:
        output_file = os.path.join(output_dir,fname)
        with open(output_file,'r') as outputfile:
            output = outputfile.read()
        sentences_json = output2json(output)
        json_file = os.path.join(json_dir,fname)
        with open(json_file, 'w') as outputjson:
    #             json.dump(problems_json, outputjson, indent = 4, separators=(',', ': '))
            json.dump(sentences_json, outputjson, indent = 4, separators=(',', ': '))



def main():
    read_file = 'res/translations'
    write_file = 'res/translations_pos'
#     build_train(read_file, write_file)

    input_name = write_file
    output_name = 'res/output'
    log_name = 'res/log'
#     count_row(fname)
    test(input_name, output_name, log_name )

#     sentence = "hello world."
#     labels2code([], sentence)

#     solution_count()
#     output_json = 'res/output_json'
#     output2json(output_name, output_json)
#     print('\n')
#     print(len(mins))
#     print(len([m for m in mins if float(m) > 0.01]))
#     print('\n')
#     solution_count(output_name, 0.01)


if __name__ == '__main__':
    main()