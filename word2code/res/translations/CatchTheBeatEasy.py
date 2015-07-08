from utils import *

class CatchTheBeatEasy:
	def ableToCatchAll(self, x, y):
		input_array0 = x
		input_array1 = y
		#  One of the modes in the game "osu!"
		# is called "catch the beat".
		# In this mode, you control a character that catches falling fruit.
		# The game is played in the vertical plane.
		# For simplicity, we will assume that both your character and all pieces of fruit are points in that plane.
		# You start the game at the coordinates (0, 0).
		# Your character can only move along the x-axis.
		# The maximum speed of your character is 1 unit of distance per second.
		# For example, you need at least 3 seconds to move from (-2, 0) to (1, 0).
		# You are given int[]s x and y that contain initial coordinates of the fruit you should catch: for each valid i, there is one piece of fruit that starts at ( x [i], y [i]).
		# All pieces of fruit fall down with constant speed of 1 unit of distance per second.
		# That is, a fruit currently located at (xf, yf) will move to (xf, yf-t) in t seconds.
		# You will catch a fruit if the character is located at the same point as the fruit at some moment in time.
		# Can you catch all the fruit in the game?
		# Return "Able to catch" (quotes for clarity) if you can, and "Not able to catch" otherwise. 
		pass

def example0():
	cls = CatchTheBeatEasy()
	input0 = [-1, 1, 0]
	input1 = [1, 3, 4]
	returns = "Able to catch"
	result = cls.ableToCatchAll(input0, input1)
	return result == returns

def example1():
	cls = CatchTheBeatEasy()
	input0 = [-3]
	input1 = [2]
	returns = "Not able to catch"
	result = cls.ableToCatchAll(input0, input1)
	return result == returns

def example2():
	cls = CatchTheBeatEasy()
	input0 = [-1, 1, 0]
	input1 = [1, 2, 4]
	returns = "Not able to catch"
	result = cls.ableToCatchAll(input0, input1)
	return result == returns

def example3():
	cls = CatchTheBeatEasy()
	input0 = [0, -1, 1]
	input1 = [9, 1, 3]
	returns = "Able to catch"
	result = cls.ableToCatchAll(input0, input1)
	return result == returns

def example4():
	cls = CatchTheBeatEasy()
	input0 = [70,-108,52,-70,84,-29,66,-33]
	input1 = [141,299,402,280,28,363,427,232]
	returns = "Not able to catch"
	result = cls.ableToCatchAll(input0, input1)
	return result == returns

def example5():
	cls = CatchTheBeatEasy()
	input0 = [-175,-28,-207,-29,-43,-183,-175,-112,-183,-31,-25,-66,-114,-116,-66]
	input1 = [320,107,379,72,126,445,318,255,445,62,52,184,247,245,185]
	returns = "Able to catch"
	result = cls.ableToCatchAll(input0, input1)
	return result == returns

def example6():
	cls = CatchTheBeatEasy()
	input0 = [0,0,0,0]
	input1 = [0,0,0,0]
	returns = "Able to catch"
	result = cls.ableToCatchAll(input0, input1)
	return result == returns

if __name__ == '__main__':
	print(example0())

