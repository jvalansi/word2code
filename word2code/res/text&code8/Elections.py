from problem_utils import *
from operator import *
import numpy


class Elections:
    def visit(self, likelihoods):
        input_array = likelihoods
        N = len(input_array)
        
        
        
        # There are two candidates campaigning to be president of a country.
        # From newspaper polls, it is clear what percentages of people plan to vote for each candidate in each state.
        # Candidate 1 wants to campaign in one last state, and needs to figure out which state that should be.
        # You are given a String[] input_array, each element of which corresponds to a state.
        # Each element consists of the characters '1' and '2', where '1' represents some number of votes for candidate 1, and '2' represents votes for candidate 2 (in each element every character represents the same number of votes).
        # You are to return an int representing the 0-based index of the state where the lowest percentage of people are planning on voting for candidate 1.
        #### possibilities = likelihoods
        possibilities = input_array
        #### def mapping(state): return percentage(state, '1')
        def mapping(possibility): return percentage(possibility, '1')
        #### def reduce(possibility): return index(possibility, lowest(possibility))
        def reduce(possibility): return indexOf(possibility, min(possibility))
        #### return reduce(map(mapping, possibilities))
        return reduce(map(mapping, possibilities))
        # (lowest percentage of '1' characters in that element of the input)
        # If there are multiple such states, return one with the lowest index in input_array.

def example0():
	cls = Elections()
	input0 = ["1222","1122","1222"]
	returns = 0
	result = cls.visit(input0)
	return result == returns

def example1():
	cls = Elections()
	input0 = ["1222111122","2222222111","11111222221222222222"]
	returns = 1
	result = cls.visit(input0)
	return result == returns

def example2():
	cls = Elections()
	input0 = ["111","112","121","122","211","212","221","222"]
	returns = 7
	result = cls.visit(input0)
	return result == returns

def example3():
	cls = Elections()
	input0 = ["1122","1221","1212","2112","2121","2211"]
	returns = 0
	result = cls.visit(input0)
	return result == returns

def example4():
	cls = Elections()
	input0 = ["11112222111121","1211221212121","112111222","11122222222111","112121222","1212122211112"]
	returns = 3
	result = cls.visit(input0)
	return result == returns

if __name__ == '__main__':
    print(example0())