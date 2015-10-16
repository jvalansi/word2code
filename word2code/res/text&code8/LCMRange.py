from problem_utils import *
from operator import *


class LCMRange:
    def lcm(self, first, last):
        input_int0 = first
        input_int1 = last
        inf = 1000
        
        
        
        
        # The least common multiple of a group of integers is the smallest number that can be evenly divided by all the integers in the group.
        def reduce0(possibility):
            #### possibilities = number(1,inf)
            possibilities = range(1, inf)
            #### def valid(possibility0): return all(evenly_divided(possibility1, number) for possibility1 in possibility)
            def valid(possibility0): return all((is_divisor(possibility1, possibility0) for possibility1 in possibility))
            #### def reduce(possibility1): return smallest(possibility0)
            def reduce(possibility0): return min(possibility0)
            #### return reduce(filter(valid, possibilities))
            return reduce(filter(valid, possibilities))
        # Given two ints, input_int0 and input_int1, find the least common multiple of all the numbers between input_int0 and input_int1, inclusive.
        #### possibilities = between(first, inclusive(last))
        possibilities = range(input_int0, inclusive(input_int1))
        #### find(least_common_multiple(possibilities))
        return reduce0(possibilities)

def example0():
    first, last = 1,5
    lcmr = LCMRange()
    result = lcmr.lcm(first, last)
    returns = 60
    return result == returns


    
if __name__ == '__main__':
    print(example0())