from utils import *

class CountryGroup:
	def solve(self, a):
		input_array = a
		#  Some people are sitting in a row.
		# Each person came here from some country.
		# You have a theory that people from the same country are all sitting together.
		# You decided to test this theory.
		# You asked each person the same question: "How many people from your country (including you) are here?"
		# You are given a int[] a containing their answers.
		# The answers are given in the order in which the people sit in the row.
		# (Note that some of the answers may be incorrect.
		# See the examples for clarification.)
		# If all the answers are consistent with your theory, return the number of different countries that are present.
		return(number(different(present(countries))))
		# (Given that all answers are consistent with the theory, the number of countries can always be uniquely determined.)
		# Otherwise, return -1. 
		pass

def example0():
	cls = CountryGroup()
	input0 = [2,2,3,3,3]
	returns = 2
	result = cls.solve(input0)
	return result == returns

def example1():
	cls = CountryGroup()
	input0 = [1,1,1,1,1]
	returns = 5
	result = cls.solve(input0)
	return result == returns

def example2():
	cls = CountryGroup()
	input0 = [3,3]
	returns = -1
	result = cls.solve(input0)
	return result == returns

def example3():
	cls = CountryGroup()
	input0 = [4,4,4,4,1,1,2,2,3,3,3]
	returns = 5
	result = cls.solve(input0)
	return result == returns

def example4():
	cls = CountryGroup()
	input0 = [2,1,2,2,1,2]
	returns = -1
	result = cls.solve(input0)
	return result == returns

if __name__ == '__main__':
	print(example0())

