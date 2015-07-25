from problem_utils import *
from operator import *

class Multiples:
    def number(self, min, max, factor):
        input_int0 = min
        input_int1 = max
        input_int2 = factor
        # You are to create a class Multiples with a method number, which takes three ints: min, max, and factor.
        
        # Given a range of integers from min to max (inclusive), determine how many numbers within that range are evenly divisible by factor.
        #### valid = lambda possibility: evenly(divisible(possibility, factor),0)
        valid = lambda possibility: eq(mod(possibility, input_int2), 0)
        #### determine(how_many([possibility for possibility in range(min, inclusive(max)) if valid(possibility)]))
        return(len([possibility for possibility in range(input_int0, inclusive(input_int1)) if valid(possibility)]))


if __name__ == '__main__':
    min = 0
    max = 14
    factor = 5
    m = Multiples()
    print(m.number(min, max, factor))