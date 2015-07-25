from problem_utils import *

class RectangleCoveringEasy:
    def solve(self, holeH, holeW, boardH, boardW):
        input_int0 = holeH
        input_int1 = holeW
        input_int2 = boardH
        input_int3 = boardW
        # There is a rectangular hole in the ground.
        # You are given the dimensions of this rectangle: ints holeH and holeW .
        # You have a rectangular board.
        # You are given its dimensions: ints boardH and boardW .
        # You would like to use the board to cover the hole.
        # There are some rules you must follow when covering the hole: You may rotate the board, but you must place it so that the sides of the board are parallel to the sides of the hole.
        may(rotate(board))
        # The board must cover the entire hole.
        # All corners of the board must be strictly outside the hole.
        # ROOT-0(root=be-7(nsubj=corners-2(det=All-1, prep_of=board-5(det=the-4)), aux=must-6, advmod=strictly-8, prep_outside=hole-11(det=the-10)))
        def can(): root=be(corners(det=All, prep_of=board), aux=must, advmod=strictly, prep_outside=hole) 
        # (That is, they are not allowed to lie on the boundary of the hole.)
        # If you can cover the hole using the board you have, return 1.
        return 1 if can else -1
        # Otherwise, return -1.



def example0():
	cls = RectangleCoveringEasy()
	input0 = 1
	input1 = 1
	input2 = 1
	input3 = 1
	returns = -1
	result = cls.solve(input0, input1, input2, input3)
	return result == returns


def example1():
	cls = RectangleCoveringEasy()
	input0 = 3
	input1 = 5
	input2 = 4
	input3 = 6
	returns = 1
	result = cls.solve(input0, input1, input2, input3)
	return result == returns


def example2():
	cls = RectangleCoveringEasy()
	input0 = 10
	input1 = 20
	input2 = 25
	input3 = 15
	returns = 1
	result = cls.solve(input0, input1, input2, input3)
	return result == returns


def example3():
	cls = RectangleCoveringEasy()
	input0 = 3
	input1 = 10
	input2 = 3
	input3 = 12
	returns = 1
	result = cls.solve(input0, input1, input2, input3)
	return result == returns



if __name__ == '__main__':
	print(example0())