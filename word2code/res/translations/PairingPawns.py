from utils import *

class PairingPawns:
	def savedPawnCount(self, start):
		input_array = start
		#  "Pairing pawns" is a game played on a strip of paper, divided into N cells.
		# The cells are labeled 0 through N-1.
		# Each cell may contain an arbitrary number of pawns.
		# You are given a int[] start with N elements.
		# For each i, element i of start is the initial number of pawns on cell i.
		# The goal of the game is to bring as many pawns as possible to cell 0.
		# The only valid move looks as follows: Find a pair of pawns that share the same cell X (other than cell 0).
		# Remove the pair of pawns from cell X.
		# Add a single new pawn into the cell X-1.
		# You may make as many moves as you wish, in any order.
		# Return the maximum number of pawns that can be in cell 0 at the end of the game. 
		pass

def example0():
	cls = PairingPawns()
	input0 = [0,2]
	returns = 1
	result = cls.savedPawnCount(input0)
	return result == returns

def example1():
	cls = PairingPawns()
	input0 = [10,3]
	returns = 11
	result = cls.savedPawnCount(input0)
	return result == returns

def example2():
	cls = PairingPawns()
	input0 = [0,0,0,8]
	returns = 1
	result = cls.savedPawnCount(input0)
	return result == returns

def example3():
	cls = PairingPawns()
	input0 = [0,1,1,2]
	returns = 1
	result = cls.savedPawnCount(input0)
	return result == returns

def example4():
	cls = PairingPawns()
	input0 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,123456]
	returns = 0
	result = cls.savedPawnCount(input0)
	return result == returns

def example5():
	cls = PairingPawns()
	input0 = [1000,2000,3000,4000,5000,6000,7000,8000]
	returns = 3921
	result = cls.savedPawnCount(input0)
	return result == returns

if __name__ == '__main__':
	print(example0())

