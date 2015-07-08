from utils import *

class MiddleCode:
	def encode(self, s):
		input_array = s
		#  Hero is learning a new algorithm to encode a string.
		# You are given a String s that consists of lowercase letters only.
		# Your task is to simulate the algorithm described below on this string, so that Hero can see how it works.
		# The algorithm starts with a given input string s and an empty output string t. The execution of the algorithm consists of multiple steps.
		# In each step, s and t are modified as follows: If the length of s is odd, the middle character of s is added to the end of t, and then deleted from s .
		# If the length of s is even, the two characters in the middle of s are compared.
		# The smaller one of them (either one in case of a tie) is added to the end of t, and then deleted from s .
		# If after some step the string s is empty, the algorithm terminates.
		# The output of the algorithm is the final string t. Return the String t that will be produced by the above algorithm for the given String s . 
		pass

def example0():
	cls = MiddleCode()
	input0 = "word"
	returns = "ordw"
	result = cls.encode(input0)
	return result == returns

def example1():
	cls = MiddleCode()
	input0 = "aaaaa"
	returns = "aaaaa"
	result = cls.encode(input0)
	return result == returns

def example2():
	cls = MiddleCode()
	input0 = "abacaba"
	returns = "caabbaa"
	result = cls.encode(input0)
	return result == returns

def example3():
	cls = MiddleCode()
	input0 = "shjegr"
	returns = "ejghrs"
	result = cls.encode(input0)
	return result == returns

def example4():
	cls = MiddleCode()
	input0 = "adafaaaadafawafwfasdaa"
	returns = "afawadafawafaafsadadaa"
	result = cls.encode(input0)
	return result == returns

if __name__ == '__main__':
	print(example0())

