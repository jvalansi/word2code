from utils import *

class MooingCows:
	def dissatisfaction(self, farmland):
		input_array = farmland
		#  The cows in Byterland are mooing loudly, annoying the residents very much.
		# Mrs. Darcy of the villa Pemberley is planning to resolve this problem by allowing only one cow to moo.
		# She will pick the cow whose mooing is the least offensive to all the other cows.
		# The farmland in Pemberley is divided into n*m squares of grassland.
		# Each square is either empty or occupied by a single cow.
		# When a cow at (x,y) moos, the dissatisfaction of a cow at (i,j) is equal to the square of the distance between them: ((x-i) 2 + (y-j) 2 ).
		# The total dissatisfaction is the sum of the dissatisfaction of all the cows.
		# Return the minimal total dissatisfaction that can be achieved by allowing only a single cow to moo.
		# The farmland will be given as a String[], where '.'
		# characters denote empty squares, and 'C' characters denote squares occupied by cows. 
		pass

def example0():
	cls = MooingCows()
	input0 = ["C..", ".C.", ".C."]
	returns = 3
	result = cls.dissatisfaction(input0)
	return result == returns

def example1():
	cls = MooingCows()
	input0 = ["CCCC", "CCCC", "CCCC"]
	returns = 26
	result = cls.dissatisfaction(input0)
	return result == returns

def example2():
	cls = MooingCows()
	input0 = ["C"]
	returns = 0
	result = cls.dissatisfaction(input0)
	return result == returns

def example3():
	cls = MooingCows()
	input0 = ["CCC....", "C......", "....C.C", ".C.CC..", "C......"]
	returns = 81
	result = cls.dissatisfaction(input0)
	return result == returns

if __name__ == '__main__':
	print(example0())

