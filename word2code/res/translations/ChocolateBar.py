from problem_utils import *

class ChocolateBar:
	def maxLength(self, letters):
		input_array = letters
		#  You just bought a very delicious chocolate bar from a local store.
		# This chocolate bar consists of N squares, numbered 0 through N-1.
		# All the squares are arranged in a single row.
		# There is a letter carved on each square.
		# You are given a String letters .
		# The i-th character of letters denotes the letter carved on the i-th square (both indices are 0-based).
		# You want to share this delicious chocolate bar with your best friend.
		# At first, you want to give him the whole bar, but then you remembered that your friend only likes a chocolate bar without repeated letters.
		# Therefore, you want to remove zero or more squares from the beginning of the bar, and then zero or more squares from the end of the bar, in such way that the remaining bar will contain no repeated letters.
		# Return the maximum possible length of the remaining chocolate bar that contains no repeated letters. 
		pass

def example0():
	cls = ChocolateBar()
	input0 = "srm"
	returns = 3
	result = cls.maxLength(input0)
	return result == returns

def example1():
	cls = ChocolateBar()
	input0 = "dengklek"
	returns = 6
	result = cls.maxLength(input0)
	return result == returns

def example2():
	cls = ChocolateBar()
	input0 = "haha"
	returns = 2
	result = cls.maxLength(input0)
	return result == returns

def example3():
	cls = ChocolateBar()
	input0 = "www"
	returns = 1
	result = cls.maxLength(input0)
	return result == returns

def example4():
	cls = ChocolateBar()
	input0 = "thisisansrmbeforetopcoderopenfinals"
	returns = 9
	result = cls.maxLength(input0)
	return result == returns

if __name__ == '__main__':
	print(example0())

