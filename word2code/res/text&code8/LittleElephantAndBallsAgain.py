from problem_utils import *
from operator import *


class LittleElephantAndBallsAgain:
    def getNumber(self, S):
        input_array = S
        N = len(input_array)
        
        
        
        # Little Elephant from the Zoo of Lviv likes balls.
        # He has some balls arranged in a row.
        # Each of those balls has one of three possible colors: red, green, or blue.
        # You are given a String input_array.
        # This string represents all the balls that are initially in the row (in the order from left to right).
        # Red, green, and blue balls are represented by characters 'R', 'G', and 'B', respectively.
        # In one turn Little Elephant can remove either the first ball in the row, or the last one.
        def mapping0(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = lambda possibility: remove(N, len(possibility))
            reduce = (lambda possibility: sub(N, len(possibility)))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # Little Elephant wants to obtain a row in which all balls have the same color.
        def valid0(possibility):
            #### possibilities = pairs(balls)
            possibilities = pairs(possibility)
            #### def mapping(possibility): return same(* pair)
            def mapping(possibility): return eq(*possibility)
            #### def reduce(possibility): return all(possibility)
            def reduce(possibility): return all(possibility)
            #### return reduce(map(mapping0, possibilities))
            return reduce(map(mapping, possibilities))
        # Return the smallest number of turns in which this can be done.
        #### possibilities = csubsets(input_array)
        possibilities = csubsets(input_array)
        #### def reduce(possibility): return smallest(possibility)
        def reduce(possibility): return min(possibility)
        #### return reduce(map(number, filter(valid0, turns)))
        return reduce(map(mapping0, filter(valid0, possibilities)))

def example0():
	cls = LittleElephantAndBallsAgain()
	input0 = "RRGGBB"
	returns = 4
	result = cls.getNumber(input0)
	return result == returns

def example1():
	cls = LittleElephantAndBallsAgain()
	input0 = "R"
	returns = 0
	result = cls.getNumber(input0)
	return result == returns

def example2():
	cls = LittleElephantAndBallsAgain()
	input0 = "RGBRGB"
	returns = 5
	result = cls.getNumber(input0)
	return result == returns

def example3():
	cls = LittleElephantAndBallsAgain()
	input0 = "RGGGBB"
	returns = 3
	result = cls.getNumber(input0)
	return result == returns

def example4():
	cls = LittleElephantAndBallsAgain()
	input0 = "RGBRBRGRGRBBBGRBRBRGBGBBBGRGBBBBRGBGRRGGRRRGRBBBBR"
	returns = 46
	result = cls.getNumber(input0)
	return result == returns

if __name__ == '__main__':
    print(example0())