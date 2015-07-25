from nltk.corpus import brown
from gensim.models import word2vec
import logging
import os
from operator import sub
import nltk


def join_files(fnames, target_fname):
    with open(target_fname, 'w') as f:
        pass
    with open(target_fname, 'a') as f:
        for fname in fnames:
            with open(fname) as f_:
                f.write(f_.read()) 

class W2V:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        name = 'text8'
        
        fname = os.path.join('res', 'GoogleNews-vectors-negative300.bin.gz')
        fname = os.path.join('res', '1-billion-word-language-modeling-benchmark-r13output.tar.gz')
        # create_model('news')
        fname = os.path.join('res', 'text8.bin')
        fname = os.path.join('res', 'brown.bin')
        fname = os.path.join('res', 'news.bin')
        self.model = word2vec.Word2Vec.load_word2vec_format(fname, binary=True)
    
    
    def create_model(self, name):
        model = word2vec.Word2Vec()
        if name == 'text8':
            sentences = word2vec.Text8Corpus(os.path.join('res', 'text8'))
            model.train(sentences)
        if name == 'brown':
        #     sentences = word2vec.BrownCorpus(fpath)
            sentences = brown.sents()
            model.train(sentences)
        if name == 'news':
            fpaths = []
            for i in range(1,100):
                fname = 'news.en-{:05}-of-00100'.format(i)
                fpaths.append(os.path.join('res', 'training-monolingual.tokenized.shuffled', fname))
            target_fpath = os.path.join('res', 'new.txt')
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
#     create_model(name)
#     model = get_model(name)
    w = W2V()
    print(w.model.similarity('subtract','difference'))

#     print(len(model.vocab.keys()))