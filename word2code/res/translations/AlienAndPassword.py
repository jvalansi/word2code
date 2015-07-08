from utils import *

class AlienAndPassword:
	def getNumber(self, S):
		input_array = S
		#  Alien Fred wants to destroy the Earth, but he forgot the password that activates the planet destroyer.
		# You are given a String S .
		# Fred remembers that the correct password can be obtained from S by erasing exactly one character.
		# Return the number of different passwords Fred needs to try. 
		pass

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
	print(example0())

