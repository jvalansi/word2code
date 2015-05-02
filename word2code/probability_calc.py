'''
Created on Jan 23, 2015

@author: jordan
'''
import re
from collections import Counter
import operator

#     get pairs of sentences, and count co-occurence of words
def calc_cooccurences(data):
    words1 = []
    words2 = []
    cooccurences = []
    for entry in data:
        if entry.code == "":
            continue
        sentence1 = entry.text.split()
        sentence2 = re.split('\s|\(|\)|\[|\]', entry.code)
        words1.extend(sentence1)
        words2.extend(sentence2)
        for word1 in sentence1:
            for word2 in sentence2:
                if word1 == '' or word2 == '':
                    continue
                cooccurences.append((word1,word2))
    words1_count = Counter(words1)
    words2_count = Counter(words2)
    cooccurences_count = Counter(cooccurences)
    cooccurences_prob = [(k,float(v)/words1_count[k[0]]) for k,v in cooccurences_count.items()]
    cooccurences_prob = dict(sorted(cooccurences_prob, key=operator.itemgetter(1)))
    return cooccurences_prob