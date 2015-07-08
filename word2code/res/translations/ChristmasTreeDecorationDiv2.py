from utils import *

class ChristmasTreeDecorationDiv2:
	def solve(self, col, x, y):
		input_array0 = col
		input_array1 = x
		input_array2 = y
		#  Christmas is just around the corner, and Alice just decorated her Christmas tree.
		# There are N stars and N-1 ribbons on the tree.
		# Each ribbon connects two of the stars in such a way that all stars and ribbons hold together.
		# (In other words, the stars and ribbons are the vertices and edges of a tree.)
		# The stars are numbered 1 through N. Additionally, each star has some color.
		# You are given the colors of stars as a int[] col with N elements.
		# For each i, col [i] is the color of star i+1.
		# (Different integers represent different colors.)
		# You are also given a description of the ribbons: two int[]s x and y with N-1 elements each.
		# For each i, there is a ribbon that connects the stars with numbers x [i] and y [i].
		# According to Alice, a ribbon that connects two stars with different colors is beautiful, while a ribbon that connects two same-colored stars is not.
		# Compute and return the number of beautiful ribbons in Alice's tree. 
		pass

def example0():
	cls = ChristmasTreeDecorationDiv2()
	input0 = [1,2,3,3]
	input1 = [1,2,3]
	input2 = [2,3,4]
	returns = 2
	result = cls.solve(input0, input1, input2)
	return result == returns

def example1():
	cls = ChristmasTreeDecorationDiv2()
	input0 = [1,3,5]
	input1 = [1,3]
	input2 = [2,2]
	returns = 2
	result = cls.solve(input0, input1, input2)
	return result == returns

def example2():
	cls = ChristmasTreeDecorationDiv2()
	input0 = [1,1,3,3]
	input1 = [1,3,2]
	input2 = [2,1,4]
	returns = 2
	result = cls.solve(input0, input1, input2)
	return result == returns

def example3():
	cls = ChristmasTreeDecorationDiv2()
	input0 = [5,5,5,5]
	input1 = [1,2,3]
	input2 = [2,3,4]
	returns = 0
	result = cls.solve(input0, input1, input2)
	return result == returns

def example4():
	cls = ChristmasTreeDecorationDiv2()
	input0 = [9,1,1]
	input1 = [3,2]
	input2 = [2,1]
	returns = 1
	result = cls.solve(input0, input1, input2)
	return result == returns

if __name__ == '__main__':
	print(example0())

