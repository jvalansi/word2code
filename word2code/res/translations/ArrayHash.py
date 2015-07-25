from problem_utils import *

class ArrayHash:
	def getHash(self, input):
		input_array = input
		#  You will be given a String[] input .
		# The value of each character in input is computed as follows: Value = (Alphabet Position) + (Element of input) + (Position in Element) All positions are 0-based.
		# 'A' has alphabet position 0, 'B' has alphabet position 1, ...
		# The returned hash is the sum of all character values in input .
		# For example, if input = {"CBA", "DDD"} then each character value would be computed as follows: 2 = 2 + 0 + 0 : 'C' in element 0 position 0 2 = 1 + 0 + 1 : 'B' in element 0 position 1 2 = 0 + 0 + 2 : 'A' in element 0 position 2 4 = 3 + 1 + 0 : 'D' in element 1 position 0 5 = 3 + 1 + 1 : 'D' in element 1 position 1 6 = 3 + 1 + 2 : 'D' in element 1 position 2 The final hash would be 2+2+2+4+5+6 = 21. 
		pass

def example0():
	cls = ArrayHash()
	input0 = ["CBA", "DDD"]
	returns = 21
	result = cls.getHash(input0)
	return result == returns

def example1():
	cls = ArrayHash()
	input0 = ["Z"]
	returns = 25
	result = cls.getHash(input0)
	return result == returns

def example2():
	cls = ArrayHash()
	input0 = ["A", "B", "C", "D", "E", "F"]
	returns = 30
	result = cls.getHash(input0)
	return result == returns

def example3():
	cls = ArrayHash()
	input0 = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
	returns = 4290
	result = cls.getHash(input0)
	return result == returns

def example4():
	cls = ArrayHash()
	input0 = ["ZZZZZZZZZZ"]
	returns = 295
	result = cls.getHash(input0)
	return result == returns

if __name__ == '__main__':
	print(example0())

