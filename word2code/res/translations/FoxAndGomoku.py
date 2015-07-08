from utils import *

class FoxAndGomoku:
	def win(self, board):
		input_array = board
		#  Fox Ciel is going to play Gomoku with her friend Fox Jiro.
		# Ciel plays better, so before they start she allowed Jiro to put some of his pieces on the board.
		# You are given a String[] board that represents a square board.
		# The character board [i][j] represents the cell with coordinates (i,j).
		# Each of those characters is either '.'
		# (representing an empty cell) or 'o' (representing a cell with Jiro's piece).
		# Of course, Ciel does not want Jiro to win the game before she has a chance to play.
		# Thus she now has to check the board and determine whether there are five consecutive tokens somewhere on the board.
		# Determine whether there are 5 consecutive cells (horizontally, vertically, or diagonally) that contain Jiro's tokens.
		# Return "found" (quotes for clarity) if there are five such cells anywhere on the board.
		# Otherwise, return "not found". 
		pass

def example0():
	cls = FoxAndGomoku()
	input0 = ["....o.", "...o..", "..o...", ".o....", "o.....", "......"]
	returns = "found"
	result = cls.win(input0)
	return result == returns

def example1():
	cls = FoxAndGomoku()
	input0 = ["oooo.", ".oooo", "oooo.", ".oooo", "....."]
	returns = "not found"
	result = cls.win(input0)
	return result == returns

def example2():
	cls = FoxAndGomoku()
	input0 = ["oooo.", ".oooo", "oooo.", ".oooo", "....o"]
	returns = "found"
	result = cls.win(input0)
	return result == returns

def example3():
	cls = FoxAndGomoku()
	input0 = ["o.....", ".o....", "..o...", "...o..", "....o.", "......"]
	returns = "found"
	result = cls.win(input0)
	return result == returns

def example4():
	cls = FoxAndGomoku()
	input0 = ["o....", "o.o..", "o.o.o", "o.o..", "o...."]
	returns = "found"
	result = cls.win(input0)
	return result == returns

def example5():
	cls = FoxAndGomoku()
	input0 = ["..........", "..........", "..oooooo..", "..o.......", "..o.......", "..oooooo..", ".......o..", ".......o..", "..oooooo..", ".........."]
	returns = "found"
	result = cls.win(input0)
	return result == returns

def example6():
	cls = FoxAndGomoku()
	input0 = ["..........", "..........", "..oooo.o..", "..o.......", "..o.......", "..o.oooo..", ".......o..", ".......o..", "..oooo.o..", ".........."]
	returns = "not found"
	result = cls.win(input0)
	return result == returns

def example7():
	cls = FoxAndGomoku()
	input0 = ["ooooo", "ooooo", "ooooo", "ooooo", "ooooo"]
	returns = "found"
	result = cls.win(input0)
	return result == returns

def example8():
	cls = FoxAndGomoku()
	input0 = [".....", ".....", ".....", ".....", "....."]
	returns = "not found"
	result = cls.win(input0)
	return result == returns

if __name__ == '__main__':
	print(example0())

