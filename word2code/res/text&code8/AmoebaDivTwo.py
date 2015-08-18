from operator import *
from problem_utils import * 


class AmoebaDivTwo:
    def count(self, table, K):
        input_array = table
        input_int = K
        
        
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
            #### def valid(possibility0): return covered(cell,amoeba)
            def valid(possibility0): return contains(possibility0, possibility)
            #### def mapping(possibility0): return contain(cell,antimatter[0])
            def mapping(possibility0): return contains(possibility0, types[0])
            #### def reduce(possibility): return every(possibility)
            def reduce(possibility): return all(possibility)
            #### return reduce(map(mapping, filter(valid, input_array)))
            return reduce(map(mapping, filter(valid, possibilities)))
        # You are given a String[] input_array, where the j-th character of the i-th element is 'A' if the cell in row i, column j of the input_array contains antimatter or 'M' if it contains matter.
        #### types = ['A','M']
        types = ['A', 'M']
        # Return the number of different ways that Romeo can place the cosmic amoeba on the input_array.
        #### possibilities = csubsets(input_array,input_int)
        possibilities = csubsets(input_array, input_int)
        #### def reduce(possibility): return number(different(possibility))
        def reduce(possibility): return len(set(possibility))
        #### return reduce(filter(can, ways))
        return reduce(filter(valid0, possibilities))
        # Two ways are considered different if and only if there is a input_array cell that is covered in one but not the other.

def example0():
    table = ['MA']
    K = 2
    adt = AmoebaDivTwo()
    returns = 0
    result = adt.count(table, K)
    return returns == result

if __name__ == '__main__':
    print(example0())