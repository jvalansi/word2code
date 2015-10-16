from problem_utils import *
from operator import *


class HammingDistance:
    def minDistance(self, numbers):
        input_array = numbers
        N = len(input_array[0])
        
        
        
        
        # The Hamming distance between two input_array is defined as the number of positions in their binary representations at which they differ (leading zeros are used if necessary to make the binary representations have the same length) -
        def mapping0(possibility):
            #### possibilities = range(N)
            possibilities = range(N)
            #### def valid(numbers): return differ(numbers[0][positions], numbers[1][positions])
            def valid(possibility0): return ne(possibility[0][possibility0], possibility[1][possibility0])
            #### def reduce(possibility0): return number(possibility0)
            def reduce(possibility0): return len(possibility0)
            #### return reduce(filter(valid, numbers))
            return reduce(filter(valid, possibilities))
        # e.g., the input_array "11010" and "01100" differ at the first, third and fourth positions, so they have a Hamming distance of 3.
        # You will be given a String[] input_array containing the binary representations of some input_array (all having the same length).
        # You are to return the minimum among the Hamming distances of all pairs of the given input_array.
        #### possibilities = pairs(numbers)
        possibilities = pairs(input_array)
        #### def reduce(possibility): return minimum(possibility)
        def reduce(possibility): return min(possibility)
        #### return reduce(map(hamming_distances, possibilities))
        return reduce(map(mapping0, possibilities))

def example0():
	cls = HammingDistance()
	input0 = ["11010", "01100"]
	returns = 3
	result = cls.minDistance(input0)
	return result == returns

def example1():
	cls = HammingDistance()
	input0 = ["00", "01", "10", "11"]
	returns = 1
	result = cls.minDistance(input0)
	return result == returns

def example2():
	cls = HammingDistance()
	input0 = ["000", "011", "101", "110"]
	returns = 2
	result = cls.minDistance(input0)
	return result == returns

def example3():
	cls = HammingDistance()
	input0 = ["01100", "01100", "10011"]
	returns = 0
	result = cls.minDistance(input0)
	return result == returns

def example4():
	cls = HammingDistance()
	input0 = ["00000000000000000000000000000000000000000000000000", "11111111111111111111111111111111111111111111111111"]
	returns = 50
	result = cls.minDistance(input0)
	return result == returns

def example5():
	cls = HammingDistance()
	input0 = ["000000", "000111", "111000", "111111"]
	returns = 3
	result = cls.minDistance(input0)
	return result == returns

if __name__ == '__main__':
    print(example0())