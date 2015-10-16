from problem_utils import *
from operator import *


class FoxAndGomoku:
    def win(self, board):
        input_array = board
        types = ['o','.']
        
        
        
        # Fox Ciel is going to play Gomoku with her friend Fox Jiro.
        # Ciel plays better, so before they start she allowed Jiro to put some of his pieces on the input_array.
        # You are given a String[] input_array that represents a square input_array.
        # The character input_array[i][j] represents the cell with coordinates (i,j).
        # Each of those characters is either '.' (representing an empty cell) or 'o' (representing a cell with Jiro's piece).
        # Of course, Ciel does not want Jiro to win the game before she has a chance to play.
        # Thus she now has to check the input_array and determine whether there are five consecutive tokens somewhere on the input_array.
        # Determine whether there are 5 consecutive cells (horizontally, vertically, or diagonally) that contain Jiro's tokens.
        def valid0(possibility):
            #### def mapping(possibility): return len(possibility)
            def mapping(possibility): return len(possibility)
            #### def valid0(possibility): return contain(tokens[0], possibility))
            def valid(possibility): return contains(types[0], possibility)
            #### def reduce(possibility): return are(possibility, 5)
            def reduce(possibility): return eq(possibility, 5)
            #### return reduce(map(mapping, filter(valid, possibility)))
            return reduce(map(mapping, filter(valid, possibilities)))
        # Return "found" (quotes for clarity) if there are five such cells anywhere on the input_array. Otherwise, return "not found".
        #### possibility = csubsets(board, five)
        possibilities = csubsets(input_array, 5)
        #### def reduce(possibility): return if(anywhere(possibility), ['found', 'not found'])
        def reduce(possibility): return if_(any(possibility), ['found', 'not found'])
        #### return reduce(filter(valid0, possibilities))
        return reduce(filter(valid0, possibilities))

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