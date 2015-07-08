from utils import *

class OnTheFarmDivTwo:
	def animals(self, heads, legs):
		input_int0 = heads
		input_int1 = legs
		#  There are some chickens and some cows in Farmer John's yard.
		# John's daughter Susie counted that all the animals in the yard have a total of 3 heads.
		# John's son Billy counted their legs and got a total of 8.
		# Using their answers, Farmer John easily determined that there have to be exactly 2 chickens and 1 cow.
		# Write a method that will solve a general version of Farmer John's problem.
		# You are given two ints heads and legs .
		# Compute the number of chickens and the number of cows.
		# Return a int[] with two elements: first the number of chickens, then the number of cows.
		# If there is no solution, return an empty int[] instead. 
		pass

def example0():
	cls = OnTheFarmDivTwo()
	input0 = 3
	input1 = 8
	returns = [2, 1 ]
	result = cls.animals(input0, input1)
	return result == returns

def example1():
	cls = OnTheFarmDivTwo()
	input0 = 10
	input1 = 40
	returns = [0, 10 ]
	result = cls.animals(input0, input1)
	return result == returns

def example2():
	cls = OnTheFarmDivTwo()
	input0 = 10
	input1 = 42
	returns = [ ]
	result = cls.animals(input0, input1)
	return result == returns

def example3():
	cls = OnTheFarmDivTwo()
	input0 = 1
	input1 = 3
	returns = [ ]
	result = cls.animals(input0, input1)
	return result == returns

def example4():
	cls = OnTheFarmDivTwo()
	input0 = 0
	input1 = 0
	returns = [0, 0 ]
	result = cls.animals(input0, input1)
	return result == returns

if __name__ == '__main__':
	print(example0())

