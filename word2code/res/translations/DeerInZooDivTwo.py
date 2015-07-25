from problem_utils import *

class DeerInZooDivTwo:
	def getminmax(self, N, K):
		input_int0 = N
		input_int1 = K
		#  Brus and Gogo came to the zoo today.
		# It's the season when deer shed their antlers.
		# There are N deer in the zoo.
		# Initially, each deer had exactly two antlers, but since then some deer may have lost one or both antlers.
		# (Now there may be some deer with two antlers, some with one, and some with no antlers at all.)
		# Brus and Gogo went through the deer enclosure and they collected all the antlers already lost by the deer.
		# The deer have lost exactly K antlers in total.
		# Brus and Gogo are now trying to calculate how many deer have not lost any antlers yet.
		# Return a int[] with exactly two elements {x,y}, where x is the smallest possible number of deer that still have two antlers, and y is the largest possible number of those deer. 
		pass

def example0():
	cls = DeerInZooDivTwo()
	input0 = 3
	input1 = 2
	returns = [1, 2 ]
	result = cls.getminmax(input0, input1)
	return result == returns

def example1():
	cls = DeerInZooDivTwo()
	input0 = 3
	input1 = 3
	returns = [0, 1 ]
	result = cls.getminmax(input0, input1)
	return result == returns

def example2():
	cls = DeerInZooDivTwo()
	input0 = 10
	input1 = 0
	returns = [10, 10 ]
	result = cls.getminmax(input0, input1)
	return result == returns

def example3():
	cls = DeerInZooDivTwo()
	input0 = 654
	input1 = 321
	returns = [333, 493 ]
	result = cls.getminmax(input0, input1)
	return result == returns

def example4():
	cls = DeerInZooDivTwo()
	input0 = 100
	input1 = 193
	returns = [0, 3 ]
	result = cls.getminmax(input0, input1)
	return result == returns

if __name__ == '__main__':
	print(example0())

