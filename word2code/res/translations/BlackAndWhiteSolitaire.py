from utils import *

class BlackAndWhiteSolitaire:
	def minimumTurns(self, cardFront):
		input_array = cardFront
		#  Manao has N cards arranged in a sequence.
		# He numbered them from left to right with numbers from 0 to N-1.
		# Each card is colored black on one side and white on the other.
		# Initially, each of the cards may lie on a different side.
		# That is, some of the cards (possibly none or all of them) will be black side up and others will be white side up.
		# Manao wants to flip some cards over to obtain an alternating configuration: every pair of successive cards must be of different colors.
		# You are given a String cardFront consisting of N characters.
		# For each i, character i of cardFront is 'B' if card i lies black side up, and 'W' otherwise.
		# Count and return the minimum number of cards which must be flipped to obtain an alternating configuration. 
		pass

def example0():
	cls = BlackAndWhiteSolitaire()
	input0 = "BBBW"
	returns = 1
	result = cls.minimumTurns(input0)
	return result == returns

def example1():
	cls = BlackAndWhiteSolitaire()
	input0 = "WBWBW"
	returns = 0
	result = cls.minimumTurns(input0)
	return result == returns

def example2():
	cls = BlackAndWhiteSolitaire()
	input0 = "WWWWWWWWW"
	returns = 4
	result = cls.minimumTurns(input0)
	return result == returns

def example3():
	cls = BlackAndWhiteSolitaire()
	input0 = "BBWBWWBWBWWBBBWBWBWBBWBBW"
	returns = 10
	result = cls.minimumTurns(input0)
	return result == returns

if __name__ == '__main__':
	print(example0())

