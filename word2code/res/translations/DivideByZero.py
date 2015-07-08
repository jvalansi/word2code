from utils import *

class DivideByZero:
	def CountNumbers(self, numbers):
		input_array = numbers
		#  Little John has a piece of paper with some distinct integers written on it.
		# You are given a int[] numbers .
		# The elements of numbers are the numbers written on John's paper.
		# John is now going to add some new numbers to his paper.
		# While doing so, he will be using integer division.
		# When doing integer division, we discard the fractional part of the result.
		# In this problem, we will use "div" to denote integer division.
		# For example, 15 div 5 = 3, and 24 div 5 = 4.
		# John will repeat the following process: He will look at his paper and select two distinct numbers A and B such that A is greater than B.
		# He will compute C = A div B.
		# If C is not written on his paper yet, he will add it to the paper.
		# The process will stop once there is no way for John to add a new number to his paper.
		# Compute and return how many numbers will there be on John's paper at the end. 
		pass

def example0():
	cls = DivideByZero()
	input0 = [9, 2]
	returns = 3
	result = cls.CountNumbers(input0)
	return result == returns

def example1():
	cls = DivideByZero()
	input0 = [8, 2]
	returns = 3
	result = cls.CountNumbers(input0)
	return result == returns

def example2():
	cls = DivideByZero()
	input0 = [50]
	returns = 1
	result = cls.CountNumbers(input0)
	return result == returns

def example3():
	cls = DivideByZero()
	input0 = [1, 5, 8, 30, 15, 4]
	returns = 11
	result = cls.CountNumbers(input0)
	return result == returns

def example4():
	cls = DivideByZero()
	input0 = [1, 2, 4, 8, 16, 32, 64]
	returns = 7
	result = cls.CountNumbers(input0)
	return result == returns

def example5():
	cls = DivideByZero()
	input0 = [6, 2, 18]
	returns = 7
	result = cls.CountNumbers(input0)
	return result == returns

if __name__ == '__main__':
	print(example0())

