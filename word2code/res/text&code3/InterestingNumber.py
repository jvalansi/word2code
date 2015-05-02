from utils import *
from operator import *
from string import digits
from numpy import where

class InterestingNumber:
    def isInteresting(self, x):
        input_array = numpy.array(x)
        # Fox Ciel thinks that the number 41312432 is interesting.
        # This is because of the following property:
        # There is exactly 1 digit between the two 1s, there are exactly 2 digits between the two 2s, and so on.
        
        # Formally, Ciel thinks that a number X is interesting if the following property is satisfied: For each D between 0 and 9, inclusive, X either does not contain the digit D at all, or it contains exactly two digits D, and there are precisely D other digits between them.
        #### interesting = lambda X: each(not contain(X, D) or (exactly(contains(X, D), two) and precisely(between(* where(eq(X, D))),int(D))) for D in between(0,inclusive(9))) 
        valid = lambda possibility: all(not contains(element, input_array) or  (eq(countOf(input_array, element), 2) and eq(sub(* where(eq(input_array, element))),int(element))) for element in range(0,inclusive(9))) 
        
        # You are given a String x that contains the digits of a positive integer.
        # Return "Interesting" if that integer is interesting, otherwise return "Not interesting".
        #### return "Interesting" if interesting(integer) otherwise "Not interesting"
        return "Interesting" if valid(input_array) else "Not interesting"
    
if __name__ == '__main__':
    x = "2002"
    In = InterestingNumber()
    print(In.isInteresting(x))