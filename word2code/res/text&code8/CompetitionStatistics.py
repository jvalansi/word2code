from problem_utils import *
from operator import *


class CompetitionStatistics:
    def consecutiveGrowth(self, ratingChanges):
        input_array = ratingChanges
        N = len(input_array)
        
        
        
        # The longest consecutive rating increase streak is a very important statistic in any competition.
        # You are to calculate this statistic for a certain player.
        # You will be given a int[] input_array containing the rating changes of the player in chronological order.
        # Your method should return the maximum number of consecutive competitions with positive rating changes.
        #### possibilities = consecutive(competitions)
        possibilities = csubsets(input_array)
        #### def mapping(possibility): return number(possibility)
        def mapping(possibility): return len(possibility)
        #### def valid(competitions): return all(map(positive ,competitions))
        def valid(possibility): return all(map(is_positive, possibility))
        #### def reduce(possibility): return maximum(possibility)
        def reduce(possibility): return max(possibility)
        #### return reduce(map(mapping, filter(valid, possibilities)))
        return reduce(map(mapping, filter(valid, possibilities)))
        # Note that 0 is not a positive number.

def example0():
	cls = CompetitionStatistics()
	input0 = [30, 5, -5, 3, 3, 1]
	returns = 3
	result = cls.consecutiveGrowth(input0)
	return result == returns

def example1():
	cls = CompetitionStatistics()
	input0 = [-1, -5, -9]
	returns = 0
	result = cls.consecutiveGrowth(input0)
	return result == returns

def example2():
	cls = CompetitionStatistics()
	input0 = [12, 0, 15, 73]
	returns = 2
	result = cls.consecutiveGrowth(input0)
	return result == returns

def example3():
	cls = CompetitionStatistics()
	input0 = [12, 1, 15, 73]
	returns = 4
	result = cls.consecutiveGrowth(input0)
	return result == returns

def example4():
	cls = CompetitionStatistics()
	input0 = [-6, 13, 15, -11, 12, 12, 33, 12, -1]
	returns = 4
	result = cls.consecutiveGrowth(input0)
	return result == returns

if __name__ == '__main__':
    print(example0())