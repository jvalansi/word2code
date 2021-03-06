from problem_utils import *
from operator import *


class MarbleDecoration:
    def maxLength(self, R, G, B):
        # Ash is a marble collector and he likes to create various ornaments using his marbles.
        # One day, Elsh asks him to create a simple decoration for her desk.
        # She wants a sequence of marbles consisting of at most two different colors.
        def valid0(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = lambda possibility: at_most(len(different(sequence)), two)
            reduce = (lambda possibility: le(len(set(possibility)), 2))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # To make the sequence look interesting, each pair of adjacent marbles must have different colors.
        def valid0(possibility):
            #### possibilities = adjacent(marbles)
            possibilities = cpairs(possibility)
            #### def mapping(possibility): return different(* possibility)
            def mapping(possibility): return diff(*possibility)
            #### def reduce(possibility): return each(possibility)
            def reduce(possibility): return all(possibility)
            #### return reduce(map(mapping, possibilities))
            return reduce(map(mapping, possibilities))
        # Currently, Ash has R red marbles, G green marbles, and B blue marbles.
        # Elsh wants that the resulting sequence is as long as possible.
        # Return this maximum length.
        #### possibilities = subsets(['red']*R + ['green']*G + ['blue']*B)
        possibilities = subsets((((['red'] * R) + (['green'] * G)) + (['blue'] * B)))
        #### def reduce(possibility): return maximum(possibility)
        def reduce(possibility): return max(possibility)
        #### def mapping(possibility): return length(possibility)
        def mapping(possibility): return len(possibility)
        #### return reduce(map(mapping, filter(valid1, filter(valid2, possibilities))))
        return reduce(map(mapping, filter(valid0, filter(valid0, possibilities))))

def example0():
	cls = MarbleDecoration()
	input0 = 0
	input1 = 0
	input2 = 0
	returns = 0
	result = cls.maxLength(input0, input1, input2)
	return result == returns

def example1():
	cls = MarbleDecoration()
	input0 = 3
	input1 = 0
	input2 = 0
	returns = 1
	result = cls.maxLength(input0, input1, input2)
	return result == returns

def example2():
	cls = MarbleDecoration()
	input0 = 5
	input1 = 1
	input2 = 2
	returns = 5
	result = cls.maxLength(input0, input1, input2)
	return result == returns

def example3():
	cls = MarbleDecoration()
	input0 = 7
	input1 = 7
	input2 = 4
	returns = 14
	result = cls.maxLength(input0, input1, input2)
	return result == returns

def example4():
	cls = MarbleDecoration()
	input0 = 2
	input1 = 3
	input2 = 5
	returns = 7
	result = cls.maxLength(input0, input1, input2)
	return result == returns

def example5():
	cls = MarbleDecoration()
	input0 = 13
	input1 = 13
	input2 = 13
	returns = 26
	result = cls.maxLength(input0, input1, input2)
	return result == returns

if __name__ == '__main__':
    print(example0())