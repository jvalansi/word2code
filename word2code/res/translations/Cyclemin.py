from utils import *

class Cyclemin:
	def bestmod(self, s, k):
		input_array = s
		input_int = k
		#  A rotation of a string S is the operation of moving its first character to the end.
		# For example, if we rotate the string "abcde" we get the string "bcdea".
		# A cyclic shift of a string S is any string that can be obtained from S by a sequence of zero or more rotations.
		# For example, the strings "abcde", "cdeab", and "eabcd" are some of the cyclic shifts of the string "abcde".
		# Given two equally long strings, the smaller one is the one with a smaller character at the first index where they differ.
		# For example, "cable" < "cards" because 'b' < 'r'.
		# You are given a String s of lowercase letters and an int k .
		# You are allowed to change at most k letters of s into some other lowercase letters.
		change = diff
		at_most = gt
		valid = lambda cyclic_shift: at_most(k, len(change(s, cyclic_shift)))
		# Your goal is to create a string that will have the smallest possible cyclic shift.
		cyclic_shift = min(cyclic_shifts)
		# Compute and return that cyclic shift. 
		return(cyclic_shift)
		pass

def example0():
	cls = Cyclemin()
	input0 = "aba"
	input1 = 1
	returns = "aaa"
	result = cls.bestmod(input0, input1)
	return result == returns

def example1():
	cls = Cyclemin()
	input0 = "aba"
	input1 = 0
	returns = "aab"
	result = cls.bestmod(input0, input1)
	return result == returns

def example2():
	cls = Cyclemin()
	input0 = "bbb"
	input1 = 2
	returns = "aab"
	result = cls.bestmod(input0, input1)
	return result == returns

def example3():
	cls = Cyclemin()
	input0 = "sgsgaw"
	input1 = 1
	returns = "aasgsg"
	result = cls.bestmod(input0, input1)
	return result == returns

def example4():
	cls = Cyclemin()
	input0 = "abacaba"
	input1 = 1
	returns = "aaaabac"
	result = cls.bestmod(input0, input1)
	return result == returns

def example5():
	cls = Cyclemin()
	input0 = "isgbiao"
	input1 = 2
	returns = "aaaisgb"
	result = cls.bestmod(input0, input1)
	return result == returns

if __name__ == '__main__':
	print(example0())

