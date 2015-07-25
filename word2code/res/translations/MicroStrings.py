from problem_utils import *

class MicroStrings:
	def makeMicroString(self, A, D):
		input_int0 = A
		input_int1 = D
		#  John couldn't handle long strings so he came up with the idea of MicroStrings.
		# You are given two positive ints: A and D .
		# These determine an infinite decreasing arithmetic progression: A , A - D , A -2 D , and so on.
		# Clearly, only finitely many elements of such a progression are non-negative.
		# Each such progression defines one MicroString, as follows: You take all the non-negative elements, convert each of them into a string, and then concatenate those strings (in order).
		# For example, let A =12 and D =5.
		# For these values we get the arithmetic progression (12, 7, 2, -3, -8, ...).
		# The non-negative elements are 12, 7, and 2.
		# The corresponding strings are "12", "7", and "2".
		# Their concatenation is the following MicroString: "1272".
		# Given A and D , return the MicroString they define. 
		pass

def example0():
	cls = MicroStrings()
	input0 = 12
	input1 = 5
	returns = "1272"
	result = cls.makeMicroString(input0, input1)
	return result == returns

def example1():
	cls = MicroStrings()
	input0 = 3
	input1 = 2
	returns = "31"
	result = cls.makeMicroString(input0, input1)
	return result == returns

def example2():
	cls = MicroStrings()
	input0 = 31
	input1 = 40
	returns = "31"
	result = cls.makeMicroString(input0, input1)
	return result == returns

def example3():
	cls = MicroStrings()
	input0 = 30
	input1 = 6
	returns = "3024181260"
	result = cls.makeMicroString(input0, input1)
	return result == returns

if __name__ == '__main__':
	print(example0())

