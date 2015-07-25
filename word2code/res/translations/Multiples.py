from problem_utils import *
from operator import *

class Multiples:
    def number(self, min, max, factor):
        input_int0 = min
        input_int1 = max
        input_int2 = factor
        
        # You are to create a class Multiples with a method number, which takes three ints: min, max, and factor.
        # Given a range of integers from min to max (inclusive), determine how many numbers within that range are evenly divisible by factor.
        #### possibilities = range(min, inclusive(max))
        possibilities = lambda possibility: subsets(possibility)
        #### valid = lambda possibility: evenly(divisible(possibility, factor))
        mapping = lambda possibility: possibility
        #### reduce = lambda possibility: how_many(possibility)
        valid = lambda possibility: possibility
        #### determine(reduce(filter(valid, possibilities)))
        reduce = lambda possibility: possibility
        return(reduce(map(mapping, filter(valid,  possibilities(input_array)))))




def example0():
    min = 0
    max = 14
    factor = 5
    m = Multiples()
    result = m.number(min, max, factor)
    returns = 3
    return result == returns


    
if __name__ == '__main__':
    print(example0())