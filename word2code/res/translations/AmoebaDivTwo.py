from utils import *

class AmoebaDivTwo:
	def count(self, table, K):
		input_array = table
		input_int = K
		#  Little Romeo likes cosmic amoebas a lot.
		# Recently he received one as a gift from his mother.
		# He decided to place his amoeba on a rectangular table.
		# The table is a grid of square 1x1 cells, and each cell is occupied by either matter or antimatter.
		# The amoeba is a rectangle of size 1x K .
		# Romeo can place it on the table in any orientation as long as every cell of the table is either completely covered by part of the amoeba or completely uncovered, and no part of the amoeba lies outside of the table.
		# It is a well-known fact that cosmic amoebas cannot lie on top of matter, so every cell of the table covered by the amoeba must only contain antimatter.
		# You are given a String[] table , where the j-th character of the i-th element is 'A' if the cell in row i, column j of the table contains antimatter or 'M' if it contains matter.
		# Return the number of different ways that Romeo can place the cosmic amoeba on the table.
		# Two ways are considered different if and only if there is a table cell that is covered in one but not the other. 
		pass

def example0():
	cls = AmoebaDivTwo()
	input0 = ["MA"]
	input1 = 2
	returns = 0
	result = cls.count(input0, input1)
	return result == returns

def example1():
	cls = AmoebaDivTwo()
	input0 = ["AAA", "AMA", "AAA"]
	input1 = 3
	returns = 4
	result = cls.count(input0, input1)
	return result == returns

def example2():
	cls = AmoebaDivTwo()
	input0 = ["AA", "AA", "AA"]
	input1 = 2
	returns = 7
	result = cls.count(input0, input1)
	return result == returns

def example3():
	cls = AmoebaDivTwo()
	input0 = ["MMM", "MMM", "MMM"]
	input1 = 1
	returns = 0
	result = cls.count(input0, input1)
	return result == returns

def example4():
	cls = AmoebaDivTwo()
	input0 = ["AAM", "MAM", "AAA"]
	input1 = 1
	returns = 6
	result = cls.count(input0, input1)
	return result == returns

def example5():
	cls = AmoebaDivTwo()
	input0 = ["AAA", "AAM", "AAA"]
	input1 = 2
	returns = 9
	result = cls.count(input0, input1)
	return result == returns

if __name__ == '__main__':
	print(example0())

