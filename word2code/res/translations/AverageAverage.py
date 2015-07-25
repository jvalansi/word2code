from problem_utils import *

class AverageAverage:
	def average(self, numList):
		input_array = numList
		#  Given a int[] numList , for each non-empty subset of numList , compute the average of its elements, then return the average of those averages. 
		pass

def example0():
	cls = AverageAverage()
	input0 = [1,2,3]
	returns = 2.0
	result = cls.average(input0)
	return result == returns

def example1():
	cls = AverageAverage()
	input0 = [42]
	returns = 42.0
	result = cls.average(input0)
	return result == returns

def example2():
	cls = AverageAverage()
	input0 = [3,1,4,15,9]
	returns = 6.4
	result = cls.average(input0)
	return result == returns

if __name__ == '__main__':
	print(example0())

