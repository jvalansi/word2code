from problem_utils import *
from operator import *


class EggCartons:
    def minCartons(self, n):
        input_int = n
        types = [6,8]
        
        
        
        # There are two types of egg cartons.
        # One type contains 6 eggs and the other type contains 8 eggs.
        # John wants to buy exactly input_int eggs.
        def valid0(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = lambda possibility: exactly(sum(possibility), input_int)
            reduce = (lambda possibility: eq(sum(possibility), input_int))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # Return the minimal number of egg cartons he must buy.
        #### possibilities = all_combinations_with_replacement(types, input_int)
        possibilities = all_combinations_with_replacement(types, input_int)
        #### def mapping(possibility): return number(possibility)
        def mapping(possibility): return len(possibility)
        #### def reduce(possibility): return minimal(possibility)
        def reduce(possibility): return min(possibility)
        #### return reduce(map(mapping, filter(valid0, egg_cartons)))
        return reduce(map(mapping, filter(valid0, possibilities)))
        # If it's impossible to buy exactly input_int eggs, return -1.\
        # if possible else -1

def example0():
	cls = EggCartons()
	input0 = 20
	returns = 3
	result = cls.minCartons(input0)
	return result == returns

def example1():
	cls = EggCartons()
	input0 = 24
	returns = 3
	result = cls.minCartons(input0)
	return result == returns

def example2():
	cls = EggCartons()
	input0 = 15
	returns = -1
	result = cls.minCartons(input0)
	return result == returns

def example3():
	cls = EggCartons()
	input0 = 4
	returns = -1
	result = cls.minCartons(input0)
	return result == returns

if __name__ == '__main__':
    print(example0())