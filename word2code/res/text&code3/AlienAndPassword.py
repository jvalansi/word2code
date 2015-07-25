from problem_utils import *
from operator import *

class AlienAndPassword:
	# Alien Fred wants to destroy the Earth, but he forgot the password that activates the planet destroyer.
	
	# You are given a String S.
	def getNumber(self, S):
		input_array = numpy.array(list(S))
		N = input_array.shape
		possibilities = subsets(input_array)

	# Fred remembers that the correct password can be obtained from S by erasing exactly one character.

	# the correct array can be done from S by removing exactly 1 element
	####	correct = lambda array: exactly(len(removing(S, array)), 1)
		valid = lambda possibility: eq(len(diff(input_array, possibility)), 1)

	# Return the number of different passwords Fred needs to try.
	####	return(number(different(possibility for possibility in passwords if valid(possibility))))
		return(len(set([possibility for possibility in possibilities if valid(possibility)])))


if __name__ == '__main__':
	S = 'aa'
	aap = AlienAndPassword()
	print(aap.getNumber(S))
