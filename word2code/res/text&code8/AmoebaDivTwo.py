from operator import *
from problem_utils import * 


class AmoebaDivTwo:
    def count(self, table, K):
        input_array = table
        input_int = K
        types = ['A', 'M']
        
        
        
        # Little Romeo likes cosmic amoebas a lot.
        # Recently he received one as a gift from his mother.
        # He decided to place his amoeba on a rectangular input_array.
        # The input_array is a grid of square 1x1 cells, and each cell is occupied by either matter or antimatter.
        # The amoeba is a rectangle of size 1xK.
        # Romeo can place it on the input_array in any orientation as long as every cell of the input_array is either completely covered by part of the amoeba or completely uncovered, and no part of the amoeba lies outside of the input_array.
        # It is a well-known fact that cosmic amoebas cannot lie on top of matter, so every cell of the input_array covered by the amoeba must only contain antimatter.
        def valid0(possibility):
            #### possibilities = input_array
            possibilities = input_array
            #### def valid(cell): return covered(cell,amoeba)
            def valid(possibility0): return contains(possibility0, possibility)
            #### def mapping(cell): return contain(cell,antimatter[0])
            def mapping(possibility0): return contains(possibility0, types[0])
            #### def reduce(cell): return every(cell)
            def reduce(possibility): return all(possibility)
            #### return reduce(map(mapping, filter(valid, input_array)))
            return reduce(map(mapping, filter(valid, possibilities)))
        # You are given a String[] input_array, where the j-th character of the i-th element is 'A' if the cell in row i, column j of the input_array contains antimatter or 'M' if it contains matter.
        # Return the number of different ways that Romeo can place the cosmic amoeba on the input_array.
        #### possibilities = csubsets(input_array,input_int)
        possibilities = csubsets(input_array, input_int)
        #### def reduce(ways): return number(different(ways))
        def reduce(possibility): return len(set(possibility))
        #### return reduce(filter(can, ways))
        return reduce(filter(valid0, possibilities))
        # Two ways are considered different if and only if there is a input_array cell that is covered in one but not the other.

def example0():
	cls = AmoebaDivTwo()
	input0 = ["MA"]
	input1 = 2
	returns = 0
	result = cls.count(input0, input1)
	return result == returns

def example1():
	cls = AmoebaDivTwo()
	input0 = ["AAA", "AMA", "AAA"]
	input1 = 3
	returns = 4
	result = cls.count(input0, input1)
	return result == returns

def example2():
	cls = AmoebaDivTwo()
	input0 = ["AA", "AA", "AA"]
	input1 = 2
	returns = 7
	result = cls.count(input0, input1)
	return result == returns

def example3():
	cls = AmoebaDivTwo()
	input0 = ["MMM", "MMM", "MMM"]
	input1 = 1
	returns = 0
	result = cls.count(input0, input1)
	return result == returns

def example4():
	cls = AmoebaDivTwo()
	input0 = ["AAM", "MAM", "AAA"]
	input1 = 1
	returns = 6
	result = cls.count(input0, input1)
	return result == returns

def example5():
	cls = AmoebaDivTwo()
	input0 = ["AAA", "AAM", "AAA"]
	input1 = 2
	returns = 9
	result = cls.count(input0, input1)
	return result == returns

if __name__ == '__main__':
    print(example0())