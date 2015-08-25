from nltk.corpus import brown
from gensim.models import word2vec
import logging
import os
import nltk
import datetime
from utils import clean_name
from multiprocessing import Pool
from six import iteritems, itervalues
from gensim.utils import smart_open, to_unicode
from numpy.core.fromnumeric import argsort


def pos_file(fname, out_fname=None):
    print(fname)
    if not out_fname:
        out_fname = fname+'.pos' 
    if os.path.exists(out_fname):
        return
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
    with open(out_fname,'w') as f:
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
    
    def get_model(self, fpath):
        return word2vec.Word2Vec.load_word2vec_format(fpath, binary=True)
        
    def create_model(self, name, max_news=99, n_proc=1):
        model = word2vec.Word2Vec(workers=n_proc)
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
            with open(target_fpath) as fp:
                s = fp.read().lower()
            with open(target_fpath, 'w') as fp:
                fp.write(s)
            sentences = word2vec.LineSentence(target_fpath)
            model.build_vocab(sentences)
            model.train(sentences)
         
    #     model.save(os.path.join('res',name+'.model'))     
        model.save_word2vec_format(os.path.join('res',name+'.bin'), binary=True)

    def log_accuracy(self, section):
        correct, incorrect = len(section['correct']), len(section['incorrect'])
        if correct + incorrect > 0:
            print("%s: %.1f%% (%i/%i)" %
                (section['section'], 100.0 * correct / (correct + incorrect),
                correct, correct + incorrect))
    
    def accuracy(self, questions, restrict_vocab=30000):
        """
        Compute accuracy of the model. `questions` is a filename where lines are
        4-tuples of words, split into sections by ": SECTION NAME" lines.
        See https://code.google.com/p/word2vec/source/browse/trunk/questions-words.txt for an example.
    
        The accuracy is reported (=printed to log and returned as a list) for each
        section separately, plus there's one aggregate summary at the end.
    
        Use `restrict_vocab` to ignore all questions containing a word whose frequency
        is not in the top-N most frequent words (default top 30,000).
    
        This method corresponds to the `compute-accuracy` script of the original C word2vec.
    
        """
        ok_vocab = dict(sorted(iteritems(self.model.vocab),
                               key=lambda item: -item[1].count)[:restrict_vocab])
        ok_index = set(v.index for v in itervalues(ok_vocab))
    
        sections, section = [], None
        for line_no, line in enumerate(smart_open(questions)):
            # TODO: use level3 BLAS (=evaluate multiple questions at once), for speed
            line = to_unicode(line)
            if line.startswith(': '):
                # a new section starts => store the old section
                if section:
                    sections.append(section)
                    self.log_accuracy(section)
                section = {'section': line.lstrip(': ').strip(), 'correct': [], 'incorrect': []}
            else:
                if not section:
                    raise ValueError("missing section header before line #%i in %s" % (line_no, questions))
                try:
                    a, b, c, expected = [word for word in line.split()]  # TODO assumes vocabulary preprocessing uses lowercase, too...
                except:
                    print("skipping invalid line #%i in %s" % (line_no, questions))
                if a not in ok_vocab or b not in ok_vocab or c not in ok_vocab or expected not in ok_vocab:
                    print("skipping line #%i with OOV words: %s" % (line_no, line.strip()))
                    continue
    
                ignore = set(self.model.vocab[v].index for v in [a, b, c])  # indexes of words to ignore
                predicted = None
                # find the most likely prediction, ignoring OOV words and input words
                positive = [b, c]
                negative = [a]
                for index in argsort(self.model.most_similar(self.model, positive, negative, False))[::-1]:
                    if index in ok_index and index not in ignore:
                        predicted = self.model.index2word[index]
                        if predicted != expected:
                            print("%s: expected %s, predicted %s" % (line.strip(), expected, predicted))
                        break
                if predicted == expected:
                    section['correct'].append((a, b, c, expected))
                else:
                    section['incorrect'].append((a, b, c, expected))
        if section:
            # store the last section, too
            sections.append(section)
            self.log_accuracy(section)
    
        total = {
            'section': 'total',
            'correct': sum((s['correct'] for s in sections), []),
            'incorrect': sum((s['incorrect'] for s in sections), []),
        }
        self.log_accuracy(total)
        sections.append(total)
        return sections

    
    def evaluate_model(self, fname):
        questions_fname = os.path.join('res', 'questions-words.txt')
        if clean_name(fname).endswith('pos'):
            pos_file(questions_fname)
            questions_fname = questions_fname+'.pos' 
        fpath = os.path.join('res', fname)
        self.model = self.get_model(fpath)
        return self.model.accuracy(questions_fname)
        
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
#     print(w2v.model.similarity('add_VB','remove_VB'))

#     print(len(model.vocab.keys()))    

    eval1 = w2v.evaluate_model('news_pos.bin')
#     eval2 = w2v.evaluate_model('news.bin')
    print(eval1)
#     print(eval2)

    
if __name__ == '__main__':
    main()