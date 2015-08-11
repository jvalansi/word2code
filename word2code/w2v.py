from nltk.corpus import brown
from gensim.models import word2vec
import logging
import os
import nltk
import datetime


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
            fname = os.path.join('res', 'GoogleNews-vectors-negative300.bin.gz')
            fname = os.path.join('res', '1-billion-word-language-modeling-benchmark-r13output.tar.gz')
            # create_model('news')
            fname = os.path.join('res', 'text8.bin')
            fname = os.path.join('res', 'brown.bin')
            fname = os.path.join('res', 'news.bin')
            fname = os.path.join('res', 'news_pos.bin')
        self.model = self.get_model(fname)
    
    def get_model(self, fname):
        return word2vec.Word2Vec.load_word2vec_format(fname, binary=True)
        
    def create_model(self, name):
        model = word2vec.Word2Vec()
        if name == 'text8':
            sentences = word2vec.Text8Corpus(os.path.join('res', 'text8'))
            model.train(sentences)
        if name == 'brown':
        #     sentences = word2vec.BrownCorpus(fpath)
            sentences = brown.sents()
            model.train(sentences)
        if name.startswith('news'):
            fpaths = []
            for i in range(1,7):
                fname = 'news.en-{:05}-of-00100'.format(i)
                if name == 'news_pos':
#                     pos_file(os.path.join('res', 'training-monolingual.tokenized.shuffled', fname))
                    fname = 'news.en-{:05}-of-00100'.format(i) + '.pos'
                fpaths.append(os.path.join('res', 'training-monolingual.tokenized.shuffled', fname))                
            target_fpath = os.path.join('res', name+'.txt')
            join_files(fpaths, target_fpath)
            sentences = word2vec.LineSentence(target_fpath)
            model.build_vocab(sentences)
            model.train(sentences)
         
    #     model.save(os.path.join('res',name+'.model'))     
        model.save_word2vec_format(os.path.join('res',name+'.bin'), binary=True)
        
    def get_similarity(self, word1, word2):
        return(self.model.similarity(word1,word2))
    

if __name__ == '__main__':
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