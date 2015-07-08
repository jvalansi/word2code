from utils import *

class TaroGrid:
    def getNumber(self, grid):
        input_array = grid
        # Cat Taro has a square grid with N rows and N columns.
        # Each cell of the grid is painted either black or white.
        # You are given a String[] grid which represents the current state of the grid.
        # Each element of grid represents one row of the grid.
        # In grid , the character 'W' represents a white cell, and the character 'B' represents a black cell.
        # Taro wants to choose a set of consecutive cells that are in the same column and are painted in the same color.
        # ROOT-0(root=wants-2(nsubj=Taro-1, xcomp=choose-4(aux=to-3, dobj=set-6(det=a-5, prep_of=cells-9(amod=consecutive-8), rcmod=are-11(nsubj=that-10, prep_in=column-15(det=the-13, amod=same-14)))), conj_and=painted-18(auxpass=are-17, prep_in=color-22(det=the-20, amod=same-21))))
        choose(set(cells(consecutive), column(same), color(same)))
        # Return the largest number of cells he can choose.
        # ROOT-0(root=choose-9(dep=Return-1(dobj=number-4(det=the-2, amod=largest-3, prep_of=cells-6)), nsubj=he-7, aux=can-8))
        return(largest(number(cells)))



def example0():
	cls = TaroGrid()
	input0 = ["W"]
	returns = 1
	result = cls.getNumber(input0)
	return result == returns


def example1():
	cls = TaroGrid()
	input0 = ["WB", "BW"]
	returns = 1
	result = cls.getNumber(input0)
	return result == returns


def example2():
	cls = TaroGrid()
	input0 = ["BWW", "BBB", "BWB"]
	returns = 3
	result = cls.getNumber(input0)
	return result == returns


def example3():
	cls = TaroGrid()
	input0 = ["BWBW", "BBWB", "WWWB", "BWWW"]
	returns = 3
	result = cls.getNumber(input0)
	return result == returns


def example4():
	cls = TaroGrid()
	input0 = ["BWB", "BBW", "BWB"]
	returns = 3
	result = cls.getNumber(input0)
	return result == returns


def example5():
	cls = TaroGrid()
	input0 = ["BBWWBBWW", "BBWWBBWW", "WWBBWWBB", "WWBBWWBB", "BBWWBBWW", "BBWWBBWW", "WWBBWWBB", "WWBBWWBB"]
	returns = 2
	result = cls.getNumber(input0)
	return result == returns



if __name__ == '__main__':
	print(example0())