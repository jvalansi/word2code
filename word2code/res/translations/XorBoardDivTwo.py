from utils import *

class XorBoardDivTwo:
    def theMax(self, board):
        input_array = board
        # Fox Jiro has a rectangular board, divided into a grid of square cells.
        # Each cell in the grid contains either the character '0', or the character '1'.
        # The String[] board contains the current state of the board.
        # The j-th character of the i-th element of board is the character in row i, column j of the grid.
        # Jiro now has to make exactly two flips.
        # In the first flip, he must pick a row and flip all characters in that row.
        first_flip = lambda row: flip(row)
        # (When flipped, a '0' turns to a '1' and vice versa.)
        flip = lambda c: '1' if c == '0' else '0'
        # In the second flip, he must pick a column and flip all characters in that column.
        second_flip = lambda column: flip(column)
        # You are given the String[] board .
        # Return the maximum number of '1's in the grid after Jiro makes the two flips.
        return(maximum(number('1', grid)))



def example0():
	cls = XorBoardDivTwo()
	input0 = ["101", "010", "101"]
	returns = 9
	result = cls.theMax(input0)
	return result == returns


def example1():
	cls = XorBoardDivTwo()
	input0 = ["111", "111", "111"]
	returns = 5
	result = cls.theMax(input0)
	return result == returns


def example2():
	cls = XorBoardDivTwo()
	input0 = ["0101001", "1101011"]
	returns = 9
	result = cls.theMax(input0)
	return result == returns


def example3():
	cls = XorBoardDivTwo()
	input0 = ["000", "001", "010", "011", "100", "101", "110", "111"]
	returns = 15
	result = cls.theMax(input0)
	return result == returns


def example4():
	cls = XorBoardDivTwo()
	input0 = ["000000000000000000000000", "011111100111111001111110", "010000000100000001000000", "010000000100000001000000", "010000000100000001000000", "011111100111111001111110", "000000100000001000000010", "000000100000001000000010", "000000100000001000000010", "011111100111111001111110", "000000000000000000000000"]
	returns = 105
	result = cls.theMax(input0)
	return result == returns



if __name__ == '__main__':
	print(example0())