'''
Created on Apr 28, 2015

@author: jordan
'''
import os
import problem2sentence
import sentence2word
import word2code
import word2codeword
import codeline_gen

def check_problems(path):
    fnames = sorted(os.listdir(path))
#     for each problem:
    for fname in fnames:        
        pass
#       identify important sentences
        
#       identify important words
#       generate code from words
    
    
if __name__ == '__main__':
    
    json_dir = 'res/phrase_json'
    problem_score = problem2sentence.calc_score(json_dir,4)
    problem_score = [os.path.splitext(fname)[0] for fname in problem_score]

    json_dir = 'res/code_json'
    word_score = sentence2word.calc_score(json_dir, 6)
    word_score = [os.path.splitext(fname)[0] for fname in word_score]
    
    codeword_score = word2codeword.check_words('res/text&code3')
    codeword_score = [os.path.splitext(fname)[0] for fname in codeword_score]

    codeline_score = codeline_gen.check_sentences('res/text&code3')
    codeline_score = [os.path.splitext(fname)[0] for fname in codeline_score]

    print(set(problem_score).intersection(set(word_score)).intersection(set(codeword_score)).intersection(codeline_score))

