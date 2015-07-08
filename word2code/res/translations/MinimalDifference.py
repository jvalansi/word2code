from utils import *

class MinimalDifference:
	def findNumber(self, A, B, C):
		input_int0 = A
		input_int1 = B
		input_int2 = C
		#  The digit sum of an integer is the sum of its digits in decimal notation.
		# For example, the digit sum of 1234 is 1+2+3+4=10, and the digit sum of 3443 is 3+4+4+3=14.
		# You are given three integers: A , B and C .
		# Return the integer X between A and B , inclusive, such that the absolute difference between the digit sum of X and the digit sum of C is as small as possible.
		# If there are multiple possible values for X, return the smallest among them. 
		pass

def example0():
	cls = MinimalDifference()
	input0 = 1
	input1 = 9
	input2 = 10
	returns = 1
	result = cls.findNumber(input0, input1, input2)
	return result == returns

def example1():
	cls = MinimalDifference()
	input0 = 11
	input1 = 20
	input2 = 20
	returns = 11
	result = cls.findNumber(input0, input1, input2)
	return result == returns

def example2():
	cls = MinimalDifference()
	input0 = 1
	input1 = 1
	input2 = 999
	returns = 1
	result = cls.findNumber(input0, input1, input2)
	return result == returns

def example3():
	cls = MinimalDifference()
	input0 = 100
	input1 = 1000
	input2 = 99
	returns = 189
	result = cls.findNumber(input0, input1, input2)
	return result == returns

def example4():
	cls = MinimalDifference()
	input0 = 1987
	input1 = 9123
	input2 = 1
	returns = 2000
	result = cls.findNumber(input0, input1, input2)
	return result == returns

if __name__ == '__main__':
	print(example0())

