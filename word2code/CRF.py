'''
Created on Feb 12, 2015

@author: jordan
'''
import subprocess
import re
import json
import os
import copy
import shutil
from utils import clean_name
from learner_wrapper import LearnerWrapper
from problem_parser import parse_problem

class Crf(LearnerWrapper):

    def label_problem(self, indir, fname, outdir, only_code=True):
        '''
        label each sentence in the problem
        
        :param problem:
        :param only_code: should sentences without code be labeled
        '''
        with open(os.path.join(indir,fname),'r') as fp:
            problem = fp.read()
        parse = parse_problem(problem)
        problem_labels = []
        for sentence_parse in parse['sentences']:
            sentence = sentence_parse['sentence']
            translations = sentence_parse['translations']
            code = sentence_parse['code']
            method = sentence_parse['method']
            if only_code and not code: #TODO: ?
                continue
    #             labels = label_sentence(sentence, translations, code)
            labels = self.label_sentence(sentence, translations, code, method)
    #         if not labels:
    #             continue
            problem_labels.append(labels)
        with open(os.path.join(outdir, clean_name(fname)+'.label'),'w') as f:
            f.write('\n\n'.join(['\n'.join(['\t'.join(label) for label in labels]) for labels in problem_labels]))
        return problem_labels 


    def join_files(self, files_dir, fnames):
        s = ''
        for fname in fnames:
            with open(os.path.join(files_dir,fname)) as infile:
                for line in infile:
                    s += line
                s += '\n\n'
        outfname = os.path.join('res', 'train')
        with open(outfname, 'w') as outfile:
            outfile.write(s)
    
    def test(self, train_dir, output_dir, test_dir=None, features=2):
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
            self.join_files(train_dir, train_fnames_)
            cmd = '/home/jordan/Downloads/CRF++-0.58/crf_learn res/features{} res/train res/model'.format(features)
            output = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
            cmd = '/home/jordan/Downloads/CRF++-0.58/crf_test -v2 -m res/model {}'.format(os.path.join(test_dir,fname))
            output = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
            sentences_json = self.output2json(output)
            json_file = os.path.join(output_dir,clean_name(fname) + '.json')
            with open(json_file, 'w') as outputjson:
                json.dump(sentences_json, outputjson, indent = 4, separators=(',', ': '))
    #         with open(os.path.join(output_dir,fname),'w') as outputfile:
    #             outputfile.write(output)
    # #             outputfile.write('----------------------\n')
    
        
    def output2json(self, output):
        prediction_pattern = r'\w+/\d\.\d+'
        named_line_pattern = r'(?P<line>(?P<word>\S+)\s+(?P<features>(?:\S+\s+)+)(?P<label>\w+)\s+(?P<prediction>'+prediction_pattern+')(?P<probs>(?:\s+'+prediction_pattern+r')+))'
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
    
    def output2json_dir(self, output_dir,json_dir):
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
            sentences_json = self.output2json(output)
            json_file = os.path.join(json_dir,clean_name(fname)+'.json')
            with open(json_file, 'w') as outputjson:
        #             json.dump(problems_json, outputjson, indent = 4, separators=(',', ': '))
                json.dump(sentences_json, outputjson, indent = 4, separators=(',', ': '))





if __name__ == '__main__':
    pass