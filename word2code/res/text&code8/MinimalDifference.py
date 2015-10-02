from problem_utils import *
from operator import *


class MinimalDifference:
    def findNumber(self, A, B, C):
        input_int0 = A
        input_int1 = B
        input_int2 = C
        
        
        
        # The digit sum of an integer is the sum of its digits in decimal notation.
        def mapping0(possibility):
            #### possibilities = str(possibility)
            possibilities = str(possibility)
            #### mapping = lambda possibility: digits(possibility)
            mapping = lambda possibility: int(possibility)
            #### reduce = lambda possibility: sum(possibility)
            reduce = lambda possibility: sum(possibility)
            #### return reduce(map(mapping, possibilities))
            return reduce(map(mapping, possibilities))
        # For example, the digit sum of 1234 is 1+2+3+4=10, and the digit sum of 3443 is 3+4+4+3=14.
        # You are given three integers: input_int0, input_int1 and input_int2.
        # Return the integer X between input_int0 and input_int1, inclusive, such that the absolute difference between the digit sum of X and the digit sum of input_int2 is as small as possible.
        # possibilities = range(input_int0,input_int1+1)
        # mapping = lambda possibility: abs(mapping1(possibility)-mapping1(input_int2))
        # valid = lambda possibility: mapping(possibility) == min(mapping(possibility) for possibility in possibilities)
        # return min(possibility for possibility in possibilities if valid(possibility))
        # If there are multiple possible values for X, return the smallest among them.
        # You are given three integers: input_int0, input_int1 and input_int2.
        # Return the integer X between input_int0 and input_int1, inclusive, such that the absolute difference between the digit sum of X and the digit sum of input_int2 is as small as possible. If there are multiple possible values for X, return the smallest among them.
        #### possibilities = between(input_int0, inclusive(input_int1))
        possibilities = range(input_int0, inclusive(input_int1))
        #### def mapping(possibility): return absolute(difference(digit_sum(possibility), digit_sum(input_int2)))
        def mapping(possibility): return abs(sub(mapping0(possibility), mapping0(input_int2)))
        #### def valid(possibility): return is(mapping(possibility), small(map(mapping, possibilities)))
        def valid(possibility): return is_(mapping(possibility), min(map(mapping, possibilities)))
        #### def reduce(possibility): return smallest(possibility)
        def reduce(possibility): return min(possibility)
        #### return reduce(filter(valid, possibilities))
        return reduce(filter(valid, possibilities))

def example0():
    A = 11
    B = 20
    C = 20
    md = MinimalDifference()
    result = md.findNumber(A, B, C)
    returns = 11
    return result == returns
    
if __name__ == '__main__':
    print(example0())