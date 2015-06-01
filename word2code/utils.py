'''
Created on Jan 27, 2015

@author: jordan
'''
from itertools import *
from operator import *

def cpairs(S):
    return csubsets(S, 2)

def pairs(S):
    return permutations(S, 2)

def subsets(S, m = None):
    N = len(S)
    if m == None:
        return chain(*map(lambda x: combinations(S, x), range(0, N+1)))
    return combinations(S, m)

def transformations(S):
    N = len(S)
    return chain(*map(lambda x: permutations(S, x), range(0, N+1)))

def csubsets(S,m = None):
    N = len(S)
    if m == None:
        return chain(S[i:i+m] for m in range(N+1) for i in range(N+1-m))
    return (S[i:i+m] for i in range(N+1-m))

def argmin(S):
    S = list(S)
    print(S)
    return S[S.index(min(S))]

def average(S):
    if not S:
        return 0
    return float(sum(S))/len(S)

def diff(S1,S2):
    return list(compress(S1,map(ne,S1,S2)))

def is_even(i):
    return i%1==0

def is_odd(i):
    return not is_even(i)

def is_prime(n):
    for i in range(3, n):
        if n % i == 0:
            return False
    return True

def is_positive(n):
    return gt(n,0)

def inclusive(n):
    return n+1

def percentage(S,n):
    return float(countOf(S, n))/len(S)

def successive(S):
    return(all(abs(pair[0]-pair[1]) == 1 for pair in cpairs(S)))

if __name__ == '__main__':
#     with open('res/logger.log','r') as fp:
#         lines = fp.readlines()
#     with open('res/sorted.log', 'w') as fp:
#         fp.write(''.join(sorted(lines)))
#     S1 = ['B','W','B','W','|','|']
#     for S in list(permutations(S1)):
#         print(list(list(s) for k,s in groupby(S,lambda x: x in '|')))
#     S2 = ['B','B','B']
#     print(list(csubsets(S1)))
#     print(list(diff(S1, S2)))
    pass