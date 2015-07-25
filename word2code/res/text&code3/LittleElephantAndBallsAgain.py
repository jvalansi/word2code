from problem_utils import *
from operator import *

class LittleElephantAndBallsAgain:
    def getNumber(self, S):
        input_array = S
        N = len(input_array)
        # Little Elephant from the Zoo of Lviv likes balls. 
        # He has some balls arranged in a row. 
        # Each of those balls has one of three possible colors: red, green, or blue.
        
        # You are given a String S. 
        # This string represents all the balls that are initially in the row (in the order from left to right). 
        # Red, green, and blue balls are represented by characters 'R', 'G', and 'B', respectively. 
        # In one turn Little Elephant can remove either the first ball in the row, or the last one. 
        possibilities = csubsets(input_array)
        mapping = lambda possibility: N - len(possibility) 
        
        # Little Elephant wants to obtain a row in which all balls have the same color.
        #### valid = lambda balls: all(same(* pair) for pair in pairs(balls))
        valid = lambda possibility: all(eq(* pair) for pair in pairs(possibility))

        # Return the smallest number of turns in which this can be done.
        #### return(smallest(number(turns) for turns in possibilities if valid(turns)))
        return(min(mapping(possibility) for possibility in possibilities if valid(possibility)))
    
if __name__ == '__main__':
    S = "RRGGBB"
    leaba = LittleElephantAndBallsAgain()
    print(leaba.getNumber(S)) 