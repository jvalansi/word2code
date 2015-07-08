from utils import *

class BichromeBoard:
	def ableToDraw(self, board):
		input_array = board
		#  We have a rectangular board divided into a grid of unit squares.
		# We are going to color each square either white or black.
		# You are given the String[] board .
		# Each character in board represents one unit square.
		# If board [i][j] is 'B', the corresponding square must be black.
		# If board [i][j] is 'W', the corresponding square must be white.
		# Finally, if board [i][j] is '?
		# ', you get to choose the color for this square: either white or black.
		# Two squares are adjacent if they share a common side.
		# We want to color the board in such a way that no two adjacent squares share the same color.
		def valid(possibility):
			two = lambda possibility: pairs(possibility)
			same = lambda possibility: eq(*possibility)
			no = lambda possibility: not(possibility)
			return(no(same(two(possibility))))
		# Return "Possible" (quotes for clarity) if it can be done, or "Impossible" otherwise.
		return  "Possible" if valid(board) else "Impossible"
		pass

def example0():
	cls = BichromeBoard()
	input0 = ["W?W", "??B", "???"]
	returns = "Possible"
	result = cls.ableToDraw(input0)
	return result == returns

def example1():
	cls = BichromeBoard()
	input0 = ["W??W"]
	returns = "Impossible"
	result = cls.ableToDraw(input0)
	return result == returns

def example2():
	cls = BichromeBoard()
	input0 = ["??"]
	returns = "Possible"
	result = cls.ableToDraw(input0)
	return result == returns

def example3():
	cls = BichromeBoard()
	input0 = ["W???", "??B?", "W???", "???W"]
	returns = "Possible"
	result = cls.ableToDraw(input0)
	return result == returns

def example4():
	cls = BichromeBoard()
	input0 = ["W???", "??B?", "W???", "?B?W"]
	returns = "Impossible"
	result = cls.ableToDraw(input0)
	return result == returns

def example5():
	cls = BichromeBoard()
	input0 = ["B"]
	returns = "Possible"
	result = cls.ableToDraw(input0)
	return result == returns

if __name__ == '__main__':
	print(example0())

