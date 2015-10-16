from problem_utils import *
from operator import *


class AlienAndPassword:
    def getNumber(self, S):
        input_array = S
        N = len(input_array)
        
        
        
        
        # Alien Fred wants to destroy the Earth, but he forgot the password that activates the planet destroyer.
        # You are given a String S.
        # Fred remembers that the correct password can be obtained from S by erasing exactly one character.
        # the correct array can be done from input_array by removing exactly 1 element
        def valid0(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = (lambda array: exactly(removing(len(input_array), len(array)), 1))
            reduce = (lambda possibility: eq(sub(len(input_array), len(possibility)), 1))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # Return the number of different passwords Fred needs to try.
        #### possibilities = subsets(input_array)
        possibilities = subsets(input_array)
        #### def reduce(passwords): return number(different(passwords))
        def reduce(possibility): return len(set(possibility))
        #### return reduce(filter(valid0, possibility))
        return reduce(filter(valid0, possibilities))

def example0():
	cls = AlienAndPassword()
	input0 = "A"
	returns = 1
	result = cls.getNumber(input0)
	return result == returns

def example1():
	cls = AlienAndPassword()
	input0 = "ABA"
	returns = 3
	result = cls.getNumber(input0)
	return result == returns

def example2():
	cls = AlienAndPassword()
	input0 = "AABACCCCABAA"
	returns = 7
	result = cls.getNumber(input0)
	return result == returns

def example3():
	cls = AlienAndPassword()
	input0 = "AGAAGAHHHHFTQLLAPUURQQRRRUFJJSBSZVJZZZ"
	returns = 26
	result = cls.getNumber(input0)
	return result == returns

def example4():
	cls = AlienAndPassword()
	input0 = "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"
	returns = 1
	result = cls.getNumber(input0)
	return result == returns

if __name__ == '__main__':
	print(example2())