'''
Created on Apr 6, 2015

@author: jordan
'''
#     extract significant phrases from problem
import nltk
from problem_parser import parse_problem
import os
import subprocess
import string
import re
import json
import ast
import CRF

# get minimal continuous subset containing all relevant words
# example:
#         sentence words: ["hello", "world", ",", "how", "are", "you", "?"]
#         relevant words: ["world", "are"]
#         smallest csubset: ["world", ",", "how", "are"]
def get_min_mask(sentwords,relevantwords):
    relevantset = set(relevantwords)
    N = len(sentwords)
    mask = [0] * N
    for i in range(N):
        for j in range(N-i):
            if relevantset.issubset(sentwords[j:j+i]):
                mask[j:j+i] = [1] * i
                return mask
    return [1] * N
                

#     input: sentence, translated code, code
#     output: labeled sentence
#     label should be according to sentence type (mapping 'M', valid 'V', return 'R') 
#     between first and last translated words, else 'O'
def label_sentence(sentence,translations,code):
    sentwords = nltk.word_tokenize(sentence.lower())
    pos = zip(*nltk.pos_tag(sentwords))[1]
    N = len(sentwords)
    labels = ['O'] * N  
    for translation,codeline in zip(translations,code):
        codewords = nltk.word_tokenize(codeline)
        transwords = nltk.word_tokenize(translation)
        if not codewords:
            continue
#         symbol = codewords[0][0].upper()
        symbol = 'I'
        relevantwords = list(set(sentwords) & set(transwords))
        relevantwords = [word for word in relevantwords if word not in string.punctuation]
        mask = get_min_mask(sentwords,relevantwords)
        if 1 not in mask:
            continue
        labels = [ symbol if mask[i] else labels[i] for i in range(N)]
        index = mask.index(1)
        labels[index] = 'B'+symbol
    return zip(sentwords,pos,labels)

def build_train(indir, outdir):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    for fname in sorted(os.listdir(indir)):
        with open(os.path.join(indir,fname),'r') as f:
            problem = f.read()
        parse = parse_problem(problem)
        sentence_labels = []
        for sentence_parse in parse['sentences']: 
            sentence = sentence_parse['sentence']
            if not sentence:
                continue
            translations = sentence_parse['translations']
            code = sentence_parse['code']
            labels = label_sentence(sentence, translations, code)
            sentence_labels.append(labels)
        fileBase, fileExtension = os.path.splitext(fname)
        with open(os.path.join(outdir,fileBase+'.label'),'w') as f:
            f.write('\n\n'.join(['\n'.join(['\t'.join(label) for label in labels]) for labels in sentence_labels]))
        
    
def calc_score(json_dir,n=4):
    correct = []
    total = 0
    fnames = sorted(os.listdir(json_dir))
    for fname in fnames:
        with open(os.path.join(json_dir,fname),'r') as inputjson:
            problem_json = json.load(inputjson)
#         with open(name,'r') as inputjson:
#             problems_json = json.load(inputjson)
#     for problem in problems_json:
#         check if n most probable sentences contain all important sentences
        sentprobs = []
        for sentence in problem_json:
            sentprob = 0
            important = False
            for line in sentence:
                if line['label'] == 'BI':
                    important = True
                probs = {v: k for k, v in ast.literal_eval(line['probs'])}
                prob = probs['BI']
                sentprob = prob if sentprob < prob else sentprob
#                 if line['prediction'][1] == 'O':
#                     continue
#                 if line['label'] == line['prediction'][1]:
#                     correct +=1
#                 total += 1
            sentprobs.append((sentprob,important))
        sentprobs = sorted(sentprobs,reverse = True)
        if all([not important for (sentprob,important) in sentprobs[n:]]):
            correct.append(fname)
        total += 1
    print(total)
    print(float(len(correct))/total)
    return correct
                
    

if __name__ == '__main__':
#     with open('res/text&code3/AmoebaDivTwo.py') as f:
#         problem = f.read()
#     parse = parse_problem(problem)
#     for sentence_parse in parse['sentences']: 
#         sentence = sentence_parse['sentence']
#         translations = sentence_parse['translations']
#         code = sentence_parse['code']
#         print(label_sentence(sentence, translations, code))

    
#     indir = 'res/text&code3/'
#     outdir = 'res/phrase_train'
#     build_train(indir, outdir)
#      
#     indir = outdir
#     outdir = 'res/phrase_test'
#     CRF.test(indir,outdir)
 
    json_dir = 'res/phrase_json'
#     CRF.output2json(outdir,json_dir)
    
    print(calc_score(json_dir,4))