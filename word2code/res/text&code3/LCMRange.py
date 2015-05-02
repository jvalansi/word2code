from utils import *
from operator import *

class LCMRange:
    def lcm(self, first, last):
        input_int0 = first
        input_int1 = last
        inf = 1000
        
        # The least common multiple of a group of integers is the smallest number that can be evenly divided by all the integers in the group.
        #### least_common_multiple = lambda group: smallest(integers for integers in group) for number in range(1, inf) if all(evenly(divided(number, integers), 0))
        reduce = lambda possibility: min(i for i in range(1, inf) if all(eq(mod(i, element), 0) for element in possibility))
              
        # Given two ints, first and last, find the least common multiple of all the numbers between first and last, inclusive.
        #### find(least_common_multiple(between(first, inclusive(last))))
        return(reduce(range(input_int0, inclusive(input_int1))))
    
if __name__ == '__main__':
    first, last = 1,5
    lcmr = LCMRange()
    print(lcmr.lcm(first, last))