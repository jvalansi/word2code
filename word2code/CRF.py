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

def parse_sentence(sentence):
    PATTERN = re.compile(r'''((?:[^"'\s]|"[^"]*"|'[^']*')+)''')
    lines = re.split('\n',sentence)
    nl = ""
    code = []
    d = {}
    missing = []
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            nl += line.strip('#').lower()
            continue
        else:
            code.append(line)
    if not nl:
        return (nl,d, missing)
    for i in range(len(code)/2):
        words = nltk.word_tokenize(code[2*i].lower())
#         words = re.sub('[,*\:\[\]\(\)\s]+',' ',code[2*i].lower())
#         words = re.split(PATTERN,words) # split on spaces except in quotes
        labels = nltk.word_tokenize(code[2*i+1].lower())
#         labels = re.sub('[,*\:\[\]\(\)\s]+',' ',code[2*i+1].lower())
#         labels = re.split(PATTERN,labels) # split on spaces except in quotes
        if len(words) != len(labels):
            continue
        for j in range(len(words)):
            key = words[j].lower()
            keys = re.split('_',key)
            value = labels[j]
            value = re.sub(r'\d','0',value)
            for key in keys:
                if key not in nltk.word_tokenize(nl):
                    missing.append(key)
                if key in string.punctuation:
                    continue
                if value == 'reduce' or value == 'valid':
                    value = 'mapping'
                d[key] = value
#     with open('code','a') as codefile:
#         codefile.write(nl + '\n')
#         codefile.write('\n'.join(code) + '\n')
#         codefile.write(str(d) + '\n')
#         codefile.write(labels2code(d, nl) + '\n')
#         codefile.write(str(set(missing)) + '\n')
#         codefile.write('\n')
    return (nl,d, missing)

def build_train(read_file,write_file):
    with open('code','w') as codefile:
        pass
    with open(read_file, 'r') as fr:
        content = fr.read()
    fw = open(write_file, 'w')
    sentences = re.split(r'\n\s*\n+', content)
    labels = []
    total_missing = []
    for sentence in sentences:
        (nl,d,missing) = parse_sentence(sentence)
        total_missing.extend(list(missing))
        labels.extend(d.values())
        text = nltk.word_tokenize(nl)
        pos = nltk.pos_tag(text)
        for element in pos:
            if element[0] in d:
                fw.write(element[0]+'\t'+element[1]+'\t'+d[element[0]]+'\n')
            else:
                fw.write(element[0]+'\t'+element[1]+'\t'+'O'+'\n')
        fw.write('\n\n')
    labels = set(labels)
    N = len(labels)
    print(N)
    print(labels)
    total_missing = Counter(total_missing)
    M = len(total_missing)
    print(M)
    print(total_missing)


def count_row(fname):
    fr = open(fname, 'r')
    lines = fr.readlines()
    for line in lines:
        if len(line.split()) not in [0,3]:
            print(line)
            print(len(line.split()))

def file2sentences(fname):
    sentence = []
    sentences = []
    with open(fname, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if len(line.split('\t')) != 3:
            if sentence:
                sentences.append(sentence)
                sentence = []
            continue
        sentence.append(line)
    if sentence:
        sentences.append(sentence)
    return sentences

def sentences2file(sentences, fname):
    with open(fname, 'w') as f:
        for sentence in sentences:
            f.write(''.join(sentence))
            f.write('\n')

def matches(line,thresh, log_name):
    s = line.split()
    orig = s[2]
    predicted = [(p.split('/')[1],p.split('/')[0]) for p in s[3:]]
    predicted = sorted(predicted,reverse = True)
#     print(predicted)
#     predicted = predicted[:5]
    predicted = [p[1] for p in predicted]
    if orig in predicted:
        index = predicted.index(orig, )
    else:
        index = len(predicted)
#     predicted = [p.split('/')[0] for p in s[3:] if float(p.split('/')[1]) > thresh]

    with open(log_name,'a') as log:
        log.write(str(s)+'\n')
#         log.write(str(orig in predicted)+'\n')
        log.write(str(index) + '\n')
    return index


def calc_score(output, log_name):
    lines = output.split('\n')
    lines = [line for line in lines if len(line.split()) >= 4]
    tagged = [line for line in lines if line.split()[2] != 'O']
    if not lines:
        return None
    match = [line for line in lines if matches(line,0.1,log_name) < 5]
    indices = [matches(line, 0.1,log_name) for line in lines]
    average_match = float(len(match))/len(lines)
    average_index = numpy.mean(indices)
    std_index = numpy.std(indices)
    with open(log_name,'a') as log:
        log.write(str(average_match)+'\n')
        log.write(str(average_index)+'\n')
        log.write(str(std_index)+'\n')
    return (average_match,average_index,std_index)

#     get the probability of each predictions
#    count calculations for the lowest probability

def get_sentence(output):
    lines = output.split('\n')
    sentence = ' '.join([line.split()[0] for line in lines if len(line.split()) >= 4])
    return sentence

def get_labels(output):
    lines = output.split('\n')
    labels = {line.split()[0]:line.split()[2] for line in lines if len(line.split()) >= 4}
    return labels

# def test(input_name, output_name, log_name):
#     sentences = file2sentences(input_name)
#     N = len(sentences)
#     print(N)
#     with open(output_name,'w') as outputfile:
#         pass
#     for i in range(N):
#         print(i)
#         sentences2file(sentences[:i]+sentences[i+1:],'res/train')
#         sentences2file([sentences[i]],'res/test')
# #         with open('res/model','w') as modelfile:
# #             pass
#         cmd = '/home/jordan/Downloads/CRF++-0.58/crf_learn res/features res/train res/model'
#         output = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
#         cmd = '/home/jordan/Downloads/CRF++-0.58/crf_test -v2 -m res/model res/test'
#         output = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
#         with open(output_name,'a') as outputfile:
#             outputfile.write(output)
#             outputfile.write('\n')


# def output2json(output_name, output_json):
#     problems = []
#     sentences = []
# #     sentence = []
#     parses = []
#     probs = []
#     mins = []
#     return_ = False
#     with open(output_name) as outputfile:
#         lines = outputfile.readlines()
#     for line in lines:
#         if not line.strip():
#             continue
#         if line.startswith('#'):
#             if probs:
#                 mins.append(min(probs))
#                 sentences.append({'parses':parses,'min':min(probs)})
#                 probs = []
#                 parses = []
#             if return_:
#                 problems.append(sentences)
#                 sentences = []
#                 return_ = False
#             continue
#         line = line.split()
#         word = line[0]
#         pos = line[1]
#         label = line[2]
#         predictions = [(element.split('/')[1], element.split('/')[0]) for element in line[3:] if element.split('/')[0] not in non_labels]
#         predictions = list(set(predictions))
#         predictions = sorted(predictions , reverse = True)
#         labels = zip(*predictions)[1]
#         if label in labels:
#             index = labels.index(label, )
#             p = predictions[index][0]
#         else:
#             index = len(labels)
#             p = 0
#         probs.append(p)
# #         parse = [word,pos,label,str(p),'\t'.join(str(p) for p in predictions[:10])]
# #         parse = {'word':word,'pos':pos,'label':label,'p':str(p),'predictions':'\t'.join(str(p) for p in predictions[:10])}
#         parse = ' '.join([word,pos,label,str(p),' '.join(str(p) for p in predictions[:4])])
#         parses.append(parse)
#         if label == 'return':
#             return_ = True
#     if probs:
#         mins.append(min(probs))
#         sentences.append({'parses':parses,'min':min(probs)})
#         probs = []
#         parses = []
#     if return_:
#         problems.append(sentences)
#         sentences = []
#         return_ = False
#     with open(output_json, 'w') as outputjson:
#         json.dump(problems, outputjson, indent = 4, separators=(',', ': '))
#     return mins

def solution_count(output_json,threshold):
    count = 0
    with open(output_json,'r') as f:
        problems = json.load(f)
    for problem in problems:
        count += all([float(sentence['min']) > threshold for sentence in problem])
    print(len(problems))
    print(count)
    return count


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
named_line_pattern = r'(?P<line>(?P<word>\S+)\s+(?P<features>(?:\S+\s+)+)(?P<label>\w+)\s+(?P<prediction>'+prediction_pattern+')\s+(?P<probs>(?:'+prediction_pattern+r'\s+)+))'
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




if __name__ == '__main__':
    read_file = 'res/translations'
    write_file = 'res/translations_pos'
    build_train(read_file, write_file)

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
    solution_count(output_name, 0.01)
