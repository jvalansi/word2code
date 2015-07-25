from problem_utils import *

class ChangingString:
	def distance(self, A, B, K):
		input_array0 = A
		input_array1 = B
		input_int = K
		#  You are given two Strings A and B that have the same length and contain only lowercase letters ('a'-'z').
		# The distance between two letters is defined as the absolute value of their difference.
		# The distance between A and B is defined as the sum of the differences between each letter in A and the letter in B at the same position.
		# For example, the distance between "abcd" and "bcda" is 6 (1 + 1 + 1 + 3).
		# You must change exactly K characters in A into other lowercase letters.
		# Return the minimum possible distance between A and B after you perform that change. 
		pass

def example0():
	cls = ChangingString()
	input0 = "ab"
	input1 = "ba"
	input2 = 2
	returns = 0
	result = cls.distance(input0, input1, input2)
	return result == returns

def example1():
	cls = ChangingString()
	input0 = "aa"
	input1 = "aa"
	input2 = 2
	returns = 2
	result = cls.distance(input0, input1, input2)
	return result == returns

def example2():
	cls = ChangingString()
	input0 = "aaa"
	input1 = "baz"
	input2 = 1
	returns = 1
	result = cls.distance(input0, input1, input2)
	return result == returns

def example3():
	cls = ChangingString()
	input0 = "fdfdfdfdfdsfabasd"
	input1 = "jhlakfjdklsakdjfk"
	input2 = 8
	returns = 24
	result = cls.distance(input0, input1, input2)
	return result == returns

def example4():
	cls = ChangingString()
	input0 = "aa"
	input1 = "bb"
	input2 = 2
	returns = 0
	result = cls.distance(input0, input1, input2)
	return result == returns

if __name__ == '__main__':
	print(example0())

