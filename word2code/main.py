'''
Created on Mar 29, 2015

@author: jordan
'''


# from utils import *
# from operator import *
# 
# class AlienAndPassword:
#     # Alien Fred wants to destroy the Earth, but he forgot the password that activates the planet destroyer.
#     # You are given a String S.
#     def getNumber(self, S):
#         input_array = numpy.array(list(S))
#         N = input_array.shape
#         possibilities = subsets(input_array)
#     # Fred remembers that the correct password can be obtained from S by erasing exactly one character.
#     # the correct array can be done from S by removing exactly 1 element
#     ####    correct = lambda array: exactly(len(removing(S, array)), 1)
#         valid = lambda possibility: eq(len(diff(input_array, possibility)), 1)
#     # Return the number of different passwords Fred needs to try.
#     ####    return(number(different(possibility for possibility in passwords if valid(possibility))))
#         return(len(set(possibility for possibility in possibilities if valid(possibility))))

#     return the number of different passwords Fred needs to try
#     dependencies:    det(number-3, the-2)
#                      prep_return(needs-8, number-3) - return(number)
#                      amod(passwords-6, different-5) - passwords = different(passwords)
#                      prep_of(number-3, passwords-6) - number = number(passwords)
#                      nsubj(needs-8, Fred-7)
#                      nsubj(try-10, Fred-7)
#                      root(ROOT-0, needs-8)
#                      aux(try-10, to-9)
#                      xcomp(needs-8, try-10)

