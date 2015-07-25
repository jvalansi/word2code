from problem_utils import *

class InterestingNumber:
	def isInteresting(self, x):
		input_array = x
		#  Fox Ciel thinks that the number 41312432 is interesting.
		# This is because of the following property: There is exactly 1 digit between the two 1s, there are exactly 2 digits between the two 2s, and so on.
		# Formally, Ciel thinks that a number X is interesting if the following property is satisfied: For each D between 0 and 9, inclusive, X either does not contain the digit D at all, or it contains exactly two digits D, and there are precisely D other digits between them.
		# You are given a String x that contains the digits of a positive integer.
		# Return "Interesting" if that integer is interesting, otherwise return "Not interesting". 
		pass

def example0():
	cls = InterestingNumber()
	input0 = "2002"
	returns = "Interesting"
	result = cls.isInteresting(input0)
	return result == returns

def example1():
	cls = InterestingNumber()
	input0 = "1001"
	returns = "Not interesting"
	result = cls.isInteresting(input0)
	return result == returns

def example2():
	cls = InterestingNumber()
	input0 = "41312432"
	returns = "Interesting"
	result = cls.isInteresting(input0)
	return result == returns

def example3():
	cls = InterestingNumber()
	input0 = "611"
	returns = "Not interesting"
	result = cls.isInteresting(input0)
	return result == returns

def example4():
	cls = InterestingNumber()
	input0 = "64200246"
	returns = "Interesting"
	result = cls.isInteresting(input0)
	return result == returns

def example5():
	cls = InterestingNumber()
	input0 = "631413164"
	returns = "Not interesting"
	result = cls.isInteresting(input0)
	return result == returns

if __name__ == '__main__':
	print(example0())

