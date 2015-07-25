from operator import *
from problem_utils import * 

class AmoebaDivTwo:
    def count(self, table, K):
        input_array = table
        input_int = K 
        possibilities = csubsets(input_array,input_int)
        # Little Romeo likes cosmic amoebas a lot.  
        # Recently he received one as a gift from his mother.  
        # He decided to place his amoeba on a rectangular table.  
        # The table is a grid of square 1x1 cells, and each cell is occupied by either matter or antimatter.  
        # The amoeba is a rectangle of size 1xK.
        # Romeo can place it on the table in any orientation as long as every cell of the table is either completely covered by part of the amoeba or completely uncovered, and no part of the amoeba lies outside of the table.
        
        # It is a well-known fact that cosmic amoebas cannot lie on top of matter, so every cell of the table covered by the amoeba must only contain antimatter.
        #### valid = lambda amoeba: every(contain(cell, antimatter[0]) for cell of table if covered(cell, amoeba))
        valid = lambda possibility: all(contains(element, types[0]) for element in input_array if contains(element, possibility))

         
        # You are given a String[] table, where the j-th character of the i-th element is 'A' if the cell in row i, column j of the table contains antimatter or 'M' if it contains matter.
        types = ['A','M']
        
        # Return the number of different ways that Romeo can place the cosmic amoeba on the table.
        #### return(number(different([possibility for possibility in ways if can(possibility)])))
        return(len(set([possibility for possibility in possibilities if valid(possibility)])))

        # Two ways are considered different if and only if there is a table cell that is covered in one but not the other.


if __name__ == '__main__':
    table = 'MA'
    K = 2
    adt = AmoebaDivTwo()
    print(adt.count(table, K))