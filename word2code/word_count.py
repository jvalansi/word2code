import os
import collections
import json
import nltk

class WordCount:
    def get_data(self,data_dir,suffix):
        data = []
        for fn in os.listdir(data_dir):
            if not fn.endswith(suffix):
                continue
            f = open(os.path.join(data_dir,fn),'r')
            data.append(f.read())
        return data

    def tuple2file(self,t,data_name):
        with open('res/count_'+data_name+'.txt', 'w') as f:
            json.dump(t, f, ensure_ascii=False, indent = 4, separators=[',',': '])

    def count_words(self,data,data_name):
        tokens = nltk.word_tokenize(data)
        c = collections.Counter(tokens)
        c = sorted(c.items(), key=lambda item: item[1],reverse = True)
        self.tuple2file(c, data_name)
        return c

    def cnt2rank(self,cnt,name):
        words,word_cnts = zip(*cnt)
        rank = enumerate(words)
        d = dict((y,x) for x,y in rank)
        self.tuple2file(tuple(rank), 'rank_'+name)
        return d


    def compare_count(self,data_dir,word):
#         rank words in problem
        prb_data = self.get_data(data_dir,'prb')
        word_cnt = self.count_words('\n'.join(prb_data), 'prb')
        word_rank = self.cnt2rank(word_cnt,'word')
        word_cnt = dict((x,y) for x,y in word_cnt)
        print(word_rank)
#         rank words in problems where solution contains word
        sol_data = self.get_data(data_dir,'sol')
        fltr_data = [prb_data[i] for i in range(len(prb_data)) if word in sol_data[i]]
        fltr_cnt = self.count_words('\n'.join(fltr_data), 'fltr')
        fltr_rank = self.cnt2rank(fltr_cnt,'fltr')
        fltr_cnt = dict((x,y) for x,y in fltr_cnt)
#         print(fltr_rank)
#          get most significant change
        print([word for word in fltr_rank if word not in word_rank])
        diff = ((word,float(fltr_cnt[word]) / word_cnt[word]) for word in fltr_cnt if word in word_cnt)
        diff = sorted(diff, key=lambda item: item[1],reverse = True)
        print(diff)
        self.tuple2file(diff, 'diff')


if __name__ == '__main__':
#     main_data_dir = 'res/brute_force_easy/'
    wc = WordCount()
#     wc.compare_count(main_data_dir, '>')

    fpath = 'res/intersection'
    with open(fpath) as f:
        data = f.read()
    wc.count_words(data, 'data') 

