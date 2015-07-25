from problem_utils import *
from operator import *

class MinimalDifference:
    def findNumber(self, A, B, C):
        input_int0 = A
        input_int1 = B
        input_int2 = C
        
        # The digit sum of an integer is the sum of its digits in decimal notation.
        #### digit_sum = lambda integer: sum(int(digits) for digits in str(integer))
        mapping1 = lambda possibility: sum(int(element) for element in str(possibility))

        # For example, the digit sum of 1234 is 1+2+3+4=10, and the digit sum of 3443 is 3+4+4+3=14.

        # You are given three integers: A, B and C.  
        # Return the integer X between A and B, inclusive, such that the absolute difference between the digit sum of X and the digit sum of C is as small as possible.
#         possibilities = range(A,B+1)
#         mapping = lambda possibility: abs(mapping1(possibility)-mapping1(C))
#         valid = lambda possibility: mapping(possibility) == min(mapping(possibility) for possibility in possibilities) 
#         return min(possibility for possibility in possibilities if valid(possibility)) 
        # If there are multiple possible values for X, return the smallest among them.
        
        # You are given three integers: A, B and C.  
        # Return the integer X between A and B, inclusive, such that the absolute difference between the digit sum of X and the digit sum of C is as small as possible.
        #### mapping = lambda possibility: absolute(difference(digit_sum(possibility), digit_sum(C)))
        mapping = lambda possibility: abs(sub(mapping1(possibility), mapping1(input_int2)))
        valid = lambda possibility: mapping(possibility) == min(mapping(possibility) for possibility in possibilities) 
        #### return(as_small_as_possible(X for X in between(A, inclusive(B)) if valid(X))) 
        return(min(possibility for possibility in range(input_int0, inclusive(input_int1)) if valid(possibility))) 
        # If there are multiple possible values for X, return the smallest among them.

        
if __name__ == '__main__':
    A = 11
    B = 20
    C = 20
    md = MinimalDifference()
    print(md.findNumber(A, B, C))