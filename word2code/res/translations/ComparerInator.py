from utils import *

class ComparerInator:
	def makeProgram(self, A, B, wanted):
		input_array0 = A
		input_array1 = B
		input_array2 = wanted
		#  Comparer-inator is a very simple language that is specialized in comparisons.
		# It takes an expression and returns the result.
		# There are only two kinds of expressions: a variable name or a tertiary operator inspired by C syntax (which is also used in many languages like Java, C++, and C#).
		# We are interested to use this language to process two int[]s, A and B to generate the int[] wanted as a result.
		# We have previously found that there are four candidate programs that could be an optimal way to solve the issue we have.
		# Each of the programs takes two arguments a and b .
		# "a" : This program will return the given argument a .
		# "b" : This program will return the given argument b .
		# "a<b?a:b" : If a is less than b, the program will return a , else it will return b .
		# "a<b?b:a" : If a is less than b, the program will return b , else it will return a .
		# Given int[] A , B and wanted find the shortest of the four candidate programs that, for every index i, will return wanted [i] after being provided a = A [i] and b = B [i] as arguments.
		# Return the length of the shortest program.
		# If no candidate program can do the required job, return -1 instead. 
		pass

def example0():
	cls = ComparerInator()
	input0 = [1]
	input1 = [2]
	input2 = [2]
	returns = 1
	result = cls.makeProgram(input0, input1, input2)
	return result == returns

def example1():
	cls = ComparerInator()
	input0 = [1,3]
	input1 = [2,1]
	input2 = [2,3]
	returns = 7
	result = cls.makeProgram(input0, input1, input2)
	return result == returns

def example2():
	cls = ComparerInator()
	input0 = [1,3,5]
	input1 = [2,1,7]
	input2 = [2,3,5]
	returns = -1
	result = cls.makeProgram(input0, input1, input2)
	return result == returns

def example3():
	cls = ComparerInator()
	input0 = [1,3,5]
	input1 = [2,1,7]
	input2 = [1,3,5]
	returns = 1
	result = cls.makeProgram(input0, input1, input2)
	return result == returns

def example4():
	cls = ComparerInator()
	input0 = [1,2,3,4,5,6,7,8,9,10,11]
	input1 = [5,4,7,8,3,1,1,2,3,4,6]
	input2 = [1,2,3,4,3,1,1,2,3,4,6]
	returns = 7
	result = cls.makeProgram(input0, input1, input2)
	return result == returns

def example5():
	cls = ComparerInator()
	input0 = [1,5,6,7,8]
	input1 = [1,5,6,7,8]
	input2 = [1,5,6,7,8]
	returns = 1
	result = cls.makeProgram(input0, input1, input2)
	return result == returns

if __name__ == '__main__':
	print(example0())

