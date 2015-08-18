from problem_utils import *
from operator import *
from string import digits
from numpy import where, array


class InterestingNumber:
    def isInteresting(self, x):
        input_array = array(x)
        
        
        # Fox Ciel thinks that the number 41312432 is interesting.
        # This is because of the following property:
        # There is exactly 1 digit between the two 1s, there are exactly 2 digits between the two 2s, and so on.
        # Formally, Ciel thinks that a number X is interesting if the following property is satisfied: For each D between 0 and 9, inclusive, X either does not contain the digit D at all, or it contains exactly two digits D, and there are precisely D other digits between them.
        def valid0(possibility):
            #### possibilities = between(0,inclusive(9))
            possibilities = range(0, inclusive(9))
            #### def mapping(possibility): return not(contain(X, D)) or (exactly(contains(X, D), two) and precisely(between(* where(eq(X, D))),int(D)))
            def mapping(possibility): return (not_(contains(input_array, possibility)) or (eq(countOf(input_array, possibility), 2) and eq(sub(*where(eq(input_array, possibility))), possibility)))
            #### def reduce(possibility): return each(possibility)
            def reduce(possibility): return all(possibility)
            #### return reduce(map(mapping, possibilities))
            return reduce(map(mapping, possibilities))
        # You are given a String x that contains the digits of a positive integer.
        # Return "Interesting" if that integer is interesting, otherwise return "Not interesting".
        #### possibilities = ["Interesting", "Not interesting"]
        possibilities = ['Interesting', 'Not interesting']
        #### reduce = lambda possibility: if_(interesting(integer), possibility)
        reduce = (lambda possibility: if_(valid0(input_array), possibility))
        #### return reduce(possibilities)
        return reduce(possibilities)

def example0():
    x = "2002"
    In = InterestingNumber()
    result = In.isInteresting(x)
    returns = "Interesting"
    return result == returns
    
if __name__ == '__main__':
    print(example0())