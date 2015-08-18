from nltk.corpus import brown
from gensim.models import word2vec
import logging
import os
import nltk
import datetime
from utils import clean_name
from multiprocessing import Pool


def pos_file(fname):
    print(fname)
    with open(fname) as f_:
        lines = f_.readlines()
        print(len(lines))
        tok_lines = [nltk.word_tokenize(sent.decode('utf-8', 'replace')) for sent in lines]
        print(datetime.datetime.now())
        new_lines = []
        for tok_line in tok_lines:
            if (tok_lines.index(tok_line))%1000 == 0:
                print(datetime.datetime.now())
                print(tok_lines.index(tok_line))
            pos_line = nltk.pos_tag(tok_line)
            new_lines.append(' '.join(['_'.join([w,p]) for w,p in pos_line]) + '\n')
    with open(fname+'.pos','w') as f:
        f.writelines([line.encode('utf-8') for line in new_lines])

def join_files(fnames, target_fname):
    with open(target_fname, 'w') as f:
        pass
    with open(target_fname, 'a') as f:
        for fname in fnames:
            print(fname)
            with open(fname) as f_:
                f.write(f_.read()) 

class W2V:
    def __init__(self, fname=None):
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        
        if not fname:
            fname = 'GoogleNews-vectors-negative300.bin.gz'
            fname = '1-billion-word-language-modeling-benchmark-r13output.tar.gz'
            # create_model('news')
            fname = 'text8.bin'
            fname = 'brown.bin'
            fname = 'news.bin'
            fname = 'news_pos.bin'
        fpath = os.path.join('res', fname)
        if not os.path.exists(fpath):
            self.create_model(clean_name(fname))
        self.model = self.get_model(fpath)
    
    def get_model(self, fname):
        return word2vec.Word2Vec.load_word2vec_format(fname, binary=True)
        
    def create_model(self, name, max_news=100, n_proc=8):
        model = word2vec.Word2Vec()
        if name == 'text8':
            sentences = word2vec.Text8Corpus(os.path.join('res', 'text8'))
            model.train(sentences)
        if name == 'brown':
        #     sentences = word2vec.BrownCorpus(fpath)
            sentences = brown.sents()
            model.train(sentences)
        if name.startswith('news'):
            fnames = ['news.en-{:05}-of-00100'.format(i+1) for i in range(max_news)]
            fpaths = [os.path.join('res', 'training-monolingual.tokenized.shuffled', fname) for fname in fnames]
            if name == 'news_pos':
                p = Pool(n_proc)
                p.map(pos_file, [fpath for fpath in fpaths if not os.path.exists(fpath+'.pos')])
#                 [pos_file(fpath) for fpath in fpaths if not os.path.exists(fpath+'.pos')]
                fpaths = [fpath+'.pos' for fpath in fpaths]
            target_fpath = os.path.join('res', name+'.txt')
            join_files(fpaths, target_fpath)
            sentences = word2vec.LineSentence(target_fpath)
            model.build_vocab(sentences)
            model.train(sentences)
         
    #     model.save(os.path.join('res',name+'.model'))     
        model.save_word2vec_format(os.path.join('res',name+'.bin'), binary=True)
        
    def get_similarity(self, word1, word2):
        return(self.model.similarity(word1,word2))
    

def main():
#     name = 'text8'
#     name = 'brown'
#     name = 'GoogleNews-vectors-negative300'
    name = 'news_pos'
    w2v = W2V()
#     w2v.create_model(name)
    print(len(w2v.model.vocab))
#     print(w2v.model.vocab.items()[:10])
    print(w2v.model.similarity('add_VB','remove_VB'))

#     print(len(model.vocab.keys()))    

if __name__ == '__main__':
    main()