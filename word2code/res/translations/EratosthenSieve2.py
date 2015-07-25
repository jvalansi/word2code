from problem_utils import *

class EratosthenSieve2:
	def nthElement(self, n):
		input_int = n
		#  Let N 1 = {1, 2, 3, 4, 5, ..., 1000} (the set of all positive integers between 1 and 1000, inclusive).
		# Delete every second number in N 1 .
		# The result is N 2 = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, ..., 999}.
		# Delete every third number in N 2 .
		# The result is N 3 = {1, 3, 7, 9, 13, 15, 19, 21, 25, ..., 999}.
		# Delete every fourth number in N 3 .
		# The result is N 4 = {1, 3, 7, 13, 15, 19, 25, 27, ...}.
		# ... Delete every tenth number in N 9 .
		# The result is N 10 .
		# Find and return the n -th element of sequence N 10 , where n is a 1-based index. 
		pass

def example0():
	cls = EratosthenSieve2()
	input0 = 3
	returns = 7
	result = cls.nthElement(input0)
	return result == returns

def example1():
	cls = EratosthenSieve2()
	input0 = 1
	returns = 1
	result = cls.nthElement(input0)
	return result == returns

def example2():
	cls = EratosthenSieve2()
	input0 = 10
	returns = 79
	result = cls.nthElement(input0)
	return result == returns

def example3():
	cls = EratosthenSieve2()
	input0 = 25
	returns = 223
	result = cls.nthElement(input0)
	return result == returns

if __name__ == '__main__':
	print(example0())

