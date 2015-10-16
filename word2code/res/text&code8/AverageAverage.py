from problem_utils import *
import string


class AverageAverage:
    def average(self, numList):
        input_array = numList
        
        
        
        
        # Given a int[] input_array, for each non-empty subset of input_array, compute the average of its elements, then return the average of those averages.
        #### possibilities = subset(input_array)
        possibilities = subsets(input_array)
        #### def valid(possibility): return possibility
        def valid(possibility): return possibility
        #### def mapping(elements): return average(elements)
        def mapping(possibility): return average(possibility)
        #### def reduce(averages): return average(averages)
        def reduce(possibility): return average(possibility)
        #### return reduce(map(mapping, filter(valid, possibilities)))
        return reduce(map(mapping, filter(valid, possibilities)))

def example0():
	cls = AverageAverage()
	input0 = [1,2,3]
	returns = 2.0
	result = cls.average(input0)
	return result == returns

def example1():
	cls = AverageAverage()
	input0 = [42]
	returns = 42.0
	result = cls.average(input0)
	return result == returns

def example2():
	cls = AverageAverage()
	input0 = [3,1,4,15,9]
	returns = 6.4
	result = cls.average(input0)
	return result == returns

if __name__ == '__main__':
    print(example0())