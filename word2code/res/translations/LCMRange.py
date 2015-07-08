from utils import *
from operator import *

class LCMRange:
    def lcm(self, first, last):
        input_int0 = first
        input_int1 = last
        inf = 1000
        
        # The least common multiple of a group of integers is the smallest number that can be evenly divided by all the integers in the group.
        def reduce(possibility):
            #### possibilities = range(1,inf)
            possibilities = lambda possibility: subsets(possibility)
            mapping = lambda possibility: possibility
            valid = lambda possibility: successive(possibility)
            reduce = lambda possibility: possibility
            return(reduce0(reduce(map(mapping, filter(valid,  possibilities(input_array))))))
        # mapping = lambda possibility1: evenly(divided(number,possibility1))
        # reduce = lambda possibility1: all(possibility1)
        # return(reduce(map(mapping, possibility)))
        # reduce = lambda possibility1: smallest(possibility0)
        # return(smallest(filter(valid, possibilities)))
        # Given two ints, first and last, find the least common multiple of all the numbers between first and last, inclusive.
        def reduce0(input_array):
            #### possibilities = between(first, inclusive(last))
            possibilities = lambda possibility: subsets(possibility)
            #### find(least_common_multiple(possibilities))
            mapping = lambda possibility: possibility
            valid = lambda possibility: possibility
            reduce = lambda possibility: possibility
            return(reduce(map(mapping, filter(valid, possibilities(input_array)))))


    
def example0():
    first, last = 1,5
    lcmr = LCMRange()
    result = lcmr.lcm(first, last)
    returns = 60
    return result == returns


    
if __name__ == '__main__':
    print(example0())