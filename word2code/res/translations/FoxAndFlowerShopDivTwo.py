from problem_utils import *

class FoxAndFlowerShopDivTwo:
	def theMaxFlowers(self, flowers, r, c):
		input_array = flowers
		input_int0 = r
		input_int1 = c
		#  Fox Jiro came to a flower shop to buy flowers.
		# The flowers in the shop are arranged in some cells of a rectangular grid.
		# The layout of the grid is given as a String[] flowers .
		# If the j-th cell of the i-th row of the grid contains a flower, then the j-th character of the i-th element of flowers will be 'F'.
		# (All indices in the previous sentence are 0-based.)
		# If the particular cell is empty, the corresponding character will be '.'
		# (a period).
		# In order to buy flowers, Jiro has to draw a rectangle on this grid and buy all the flowers which lie inside the rectangle.
		# Of course, the sides of the rectangle must be on cell boundaries.
		# (Therefore, the sides of the rectangle will necessarily be parallel to the coordinate axes.)
		# Jiro wants to buy as many flowers as possible.
		# Unfortunately, he cannot select the entire grid.
		# Eel Saburo came to this shop before Jiro.
		# Saburo has already drawn his rectangle.
		# Saburo's rectangle contains just a single cell: the c -th cell of the r -th row of the grid.
		# (Again, both indices are 0-based.)
		# Jiro's rectangle may not contain this cell.
		# You are given the String[] flowers and the ints r and c .
		# Return the maximum possible number of flowers Jiro can buy in this situation. 
		pass

def example0():
	cls = FoxAndFlowerShopDivTwo()
	input0 = ["F.F", ".F.", ".F."]
	input1 = 1
	input2 = 1
	returns = 2
	result = cls.theMaxFlowers(input0, input1, input2)
	return result == returns

def example1():
	cls = FoxAndFlowerShopDivTwo()
	input0 = ["F..", "...", "..."]
	input1 = 0
	input2 = 0
	returns = 0
	result = cls.theMaxFlowers(input0, input1, input2)
	return result == returns

def example2():
	cls = FoxAndFlowerShopDivTwo()
	input0 = [".FF.F.F", "FF...F.", "..FF.FF"]
	input1 = 1
	input2 = 2
	returns = 6
	result = cls.theMaxFlowers(input0, input1, input2)
	return result == returns

def example3():
	cls = FoxAndFlowerShopDivTwo()
	input0 = ["F", ".", "F", "F", "F", ".", "F", "F"]
	input1 = 4
	input2 = 0
	returns = 3
	result = cls.theMaxFlowers(input0, input1, input2)
	return result == returns

def example4():
	cls = FoxAndFlowerShopDivTwo()
	input0 = [".FFF..F...", "FFF...FF.F", "..F.F.F.FF", "FF..F.FFF.", "..FFFFF...", "F....FF...", ".FF.FF..FF", "..F.F.FFF.", ".FF..F.F.F", "F.FFF.FF.F"]
	input1 = 4
	input2 = 3
	returns = 32
	result = cls.theMaxFlowers(input0, input1, input2)
	return result == returns

if __name__ == '__main__':
	print(example0())

