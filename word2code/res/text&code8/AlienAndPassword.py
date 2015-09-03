from problem_utils import *
from operator import *


class AlienAndPassword:
    def getNumber(self, S):
        input_array = S
        N = len(input_array)
        
        
        
        # Alien Fred wants to destroy the Earth, but he forgot the password that activates the planet destroyer.
        # You are given a String S.
        # Fred remembers that the correct password can be obtained from S by erasing exactly one character.
        # the correct array can be done from S by removing exactly 1 element
        def valid0(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = (lambda array: exactly(len(removing(S, array)), 1))
            reduce = (lambda possibility: eq(len(diff(input_array, possibility)), 1))
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
	S = 'aa'
	aap = AlienAndPassword()
	returns = 1
	result = aap.getNumber(S)
	return returns == result

if __name__ == '__main__':
	print(example0())