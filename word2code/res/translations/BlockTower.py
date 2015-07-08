from utils import *

class BlockTower:
	def getTallest(self, blockHeights):
		input_array = blockHeights
		#  Josh loves playing with blocks.
		# Currently, he has N blocks, labeled 0 through N-1.
		# The heights of all blocks are positive integers.
		# More precisely, for each i, the height of block i is blockHeights [i].
		# Josh is interested in making the tallest block tower possible.
		# He likes all his towers to follow three simple rules: The blocks must be stacked in a single column, one atop another.
		# The height of the tower is simply the sum of heights of all its blocks.
		# The labels of blocks used in the tower must increase from the bottom to the top.
		# In other words, whenever Josh places box x on top of box y, we have x > y. Josh will never place a box of an even height on top of a box of an odd height.
		# You are given the int[] blockHeights .
		# Return the height of the tallest possible block tower Josh can build. 
		pass

def example0():
	cls = BlockTower()
	input0 = [4,7]
	returns = 11
	result = cls.getTallest(input0)
	return result == returns

def example1():
	cls = BlockTower()
	input0 = [7,4]
	returns = 7
	result = cls.getTallest(input0)
	return result == returns

def example2():
	cls = BlockTower()
	input0 = [7]
	returns = 7
	result = cls.getTallest(input0)
	return result == returns

def example3():
	cls = BlockTower()
	input0 = [4]
	returns = 4
	result = cls.getTallest(input0)
	return result == returns

def example4():
	cls = BlockTower()
	input0 = [48,1,50,1,50,1,48]
	returns = 196
	result = cls.getTallest(input0)
	return result == returns

def example5():
	cls = BlockTower()
	input0 = [49,2,49,2,49]
	returns = 147
	result = cls.getTallest(input0)
	return result == returns

def example6():
	cls = BlockTower()
	input0 = [44,3,44,3,44,47,2,47,2,47,2]
	returns = 273
	result = cls.getTallest(input0)
	return result == returns

if __name__ == '__main__':
	print(example0())

