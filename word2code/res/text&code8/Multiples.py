from problem_utils import *
from operator import *


class Multiples:
    def number(self, min, max, factor):
        input_int0 = min
        input_int1 = max
        input_int2 = factor
        
        
        
        # You are to create a class Multiples with a method number, which takes three ints: input_int0, input_int1, and input_int2.
        # Given a range of integers from input_int0 to input_int1 (inclusive), determine how many numbers within that range are evenly divisible by input_int2.
        #### possibilities = range(input_int0, inclusive(input_int1))
        possibilities = range(input_int0, inclusive(input_int1))
        #### def valid(possibility): return divisible(input_int2, possibility)
        def valid(possibility): return is_divisor(input_int2, possibility)
        #### def reduce(possibility): return how_many(possibility)
        def reduce(possibility): return len(possibility)
        #### determine(reduce(filter(valid, possibilities)))
        return reduce(filter(valid, possibilities))

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