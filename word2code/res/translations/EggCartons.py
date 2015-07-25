from problem_utils import *

class EggCartons:
	def minCartons(self, n):
		input_int = n
		#  There are two types of egg cartons.
		# One type contains 6 eggs and the other type contains 8 eggs.
		# John wants to buy exactly n eggs.
		# Return the minimal number of egg cartons he must buy.
		# If it's impossible to buy exactly n eggs, return -1. 
		pass

def example0():
	cls = EggCartons()
	input0 = 20
	returns = 3
	result = cls.minCartons(input0)
	return result == returns

def example1():
	cls = EggCartons()
	input0 = 24
	returns = 3
	result = cls.minCartons(input0)
	return result == returns

def example2():
	cls = EggCartons()
	input0 = 15
	returns = -1
	result = cls.minCartons(input0)
	return result == returns

def example3():
	cls = EggCartons()
	input0 = 4
	returns = -1
	result = cls.minCartons(input0)
	return result == returns

if __name__ == '__main__':
	print(example0())

