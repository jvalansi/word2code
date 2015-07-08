from utils import *

class SurroundingGameEasy:
    def score(self, cost, benefit, stone):
        input_array0 = cost
        input_array1 = benefit
        input_array2 = stone
        # Surrounding Game is a single-player game played on a rectangular grid of cells.
        # Cells are considered adjacent if they share a common side.
        # ROOT-0(root=considered-3(nsubjpass=Cells-1, auxpass=are-2, acomp=adjacent-4, advcl=share-7(mark=if-5, nsubj=they-6, dobj=side-10(det=a-8, amod=common-9))))
        # (Hence, each cell has at most four adjacent cells.
        # The cells on the sides and in the corners of the grid have fewer adjacent cells than the ones inside the grid.)
        # The game is played by placing stones into some of the cells.
        # Each cell may only contain at most one stone.
        # A cell is called dominated if at least one of the following two conditions holds: The cell contains a stone.
        at_least = ge
        one = 1
        def dominated(cell): return at_least(one, sum(conditions(cell)))
        def conditions(cell): return [contains(cell, stone),]
        # All cells adjacent to the cell contain stones.
        def valid(cell): return all(contain(cell, stone) for cell in adjacent(cell))
        # Each cell of the grid contains two numbers, each from 0 to 9, inclusive: the cost of placing a stone into the cell, and the benefit from dominating the cell.
        # At the end of the game, the overall score of the player is the sum of all benefits minus the sum of all costs.
        score = minus(sum(benefits), sum(costs))
        # You are given the String[]s cost and benefit .
        # The characters cost [i][j] and benefit [i][j] represent the two digits written in the cell (i,j).
        # For example, if character 7 of element 4 of cost is '3', the cost of placing a stone into the cell (4,7) is 3.
        # You are also given a String[] stone that describes the final state of the game.
        # The character stone [i][j] is 'o' (lowercase letter oh) if the cell (i,j) contains a stone.
        def contain((i,j), stone): stone[i][j] == 'o'
        # Otherwise, stone [i][j] is '.'
        # (a period).
        # Calculate and return the overall score of the game.
        return(score)



def example0():
	cls = SurroundingGameEasy()
	input0 = ["21","12"]
	input1 = ["21","12"]
	input2 = [".o","o."]
	returns = 4
	result = cls.score(input0, input1, input2)
	return result == returns


def example1():
	cls = SurroundingGameEasy()
	input0 = ["99","99"]
	input1 = ["11","11"]
	input2 = [".o","o."]
	returns = -14
	result = cls.score(input0, input1, input2)
	return result == returns


def example2():
	cls = SurroundingGameEasy()
	input0 = ["888","888","888"]
	input1 = ["000","090","000"]
	input2 = ["...",".o.","..."]
	returns = 1
	result = cls.score(input0, input1, input2)
	return result == returns


def example3():
	cls = SurroundingGameEasy()
	input0 = ["4362","4321"]
	input1 = ["5329","5489"]
	input2 = ["...o","..o."]
	returns = 22
	result = cls.score(input0, input1, input2)
	return result == returns


def example4():
	cls = SurroundingGameEasy()
	input0 = ["5413","4323","8321","5490"]
	input1 = ["0432","7291","3901","2310"]
	input2 = ["ooo.","o..o","...o","oooo"]
	returns = -12
	result = cls.score(input0, input1, input2)
	return result == returns



if __name__ == '__main__':
	print(example0())