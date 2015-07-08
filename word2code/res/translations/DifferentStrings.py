from utils import *

class DifferentStrings:
	def minimize(self, A, B):
		input_array0 = A
		input_array1 = B
		#  If X and Y are two Strings of equal length N, then the difference between them is defined as the number of indices i where the i-th character of X and the i-th character of Y are different.
		# For example, the difference between the words "ant" and "art" is 1.
		# You are given two Strings, A and B , where the length of A is less than or equal to the length of B .
		# You can apply an arbitrary number of operations to A , where each operation is one of the following: Choose a character c and add it to the beginning of A .
		# Choose a character c and add it to the end of A .
		# Apply the operations in such a way that A and B have the same length and the difference between them is as small as possible.
		# Return this minimum possible difference. 
		pass

def example0():
	cls = DifferentStrings()
	input0 = "koder"
	input1 = "topcoder"
	returns = 1
	result = cls.minimize(input0, input1)
	return result == returns

def example1():
	cls = DifferentStrings()
	input0 = "hello"
	input1 = "xello"
	returns = 1
	result = cls.minimize(input0, input1)
	return result == returns

def example2():
	cls = DifferentStrings()
	input0 = "abc"
	input1 = "topabcoder"
	returns = 0
	result = cls.minimize(input0, input1)
	return result == returns

def example3():
	cls = DifferentStrings()
	input0 = "adaabc"
	input1 = "aababbc"
	returns = 2
	result = cls.minimize(input0, input1)
	return result == returns

def example4():
	cls = DifferentStrings()
	input0 = "giorgi"
	input1 = "igroig"
	returns = 6
	result = cls.minimize(input0, input1)
	return result == returns

if __name__ == '__main__':
	print(example0())

