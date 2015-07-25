from problem_utils import *

class LittleElephantAndBallsAgain:
	def getNumber(self, S):
		input_array = S
		#  Little Elephant from the Zoo of Lviv likes balls.
		# He has some balls arranged in a row.
		# Each of those balls has one of three possible colors: red, green, or blue.
		# You are given a String S .
		# This string represents all the balls that are initially in the row (in the order from left to right).
		# Red, green, and blue balls are represented by characters 'R', 'G', and 'B', respectively.
		# In one turn Little Elephant can remove either the first ball in the row, or the last one.
		# Little Elephant wants to obtain a row in which all balls have the same color.
		# Return the smallest number of turns in which this can be done. 
		pass

def example0():
	cls = LittleElephantAndBallsAgain()
	input0 = "RRGGBB"
	returns = 4
	result = cls.getNumber(input0)
	return result == returns

def example1():
	cls = LittleElephantAndBallsAgain()
	input0 = "R"
	returns = 0
	result = cls.getNumber(input0)
	return result == returns

def example2():
	cls = LittleElephantAndBallsAgain()
	input0 = "RGBRGB"
	returns = 5
	result = cls.getNumber(input0)
	return result == returns

def example3():
	cls = LittleElephantAndBallsAgain()
	input0 = "RGGGBB"
	returns = 3
	result = cls.getNumber(input0)
	return result == returns

def example4():
	cls = LittleElephantAndBallsAgain()
	input0 = "RGBRBRGRGRBBBGRBRBRGBGBBBGRGBBBBRGBGRRGGRRRGRBBBBR"
	returns = 46
	result = cls.getNumber(input0)
	return result == returns

if __name__ == '__main__':
	print(example0())

