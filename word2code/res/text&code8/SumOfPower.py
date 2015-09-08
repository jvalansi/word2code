from problem_utils import *


class SumOfPower:
    def findSum(self, array):
        input_array = array
        
        
        # You are given a int[] input_array .
        # At any moment, you may choose a nonempty contiguous subsequence of input_array .
        #### possibilities = subsequence(input_array)
        possibilities = csubsets(input_array)
        # Whenever you do so, you will gain power equal to the sum of all elements in the chosen subsequence.
        def mapping0(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### def reduce(possibility): return sum(possibility)
            def reduce(possibility): return sum(possibility)
            #### return reduce(subsequence)
            return reduce(possibilities)
        # You chose each possible contiguous subsequence exactly once, each time gaining some power.
        # Compute and return the total amount of power you gained.
        #### def reduce(total): return sum(possibility)
        def reduce(possibility): return sum(possibility)
        #### return reduce(map(power, possibilities))
        return reduce(map(mapping0, possibilities))

def example0():
	cls = SumOfPower()
	input0 = [1,2]
	returns = 6
	result = cls.findSum(input0)
	return result == returns


def example1():
	cls = SumOfPower()
	input0 = [1,1,1]
	returns = 10
	result = cls.findSum(input0)
	return result == returns


def example2():
	cls = SumOfPower()
	input0 = [3,14,15,92,65]
	returns = 1323
	result = cls.findSum(input0)
	return result == returns


def example3():
	cls = SumOfPower()
	input0 = [1,2,3,4,5,6,7,8,9,10]
	returns = 1210
	result = cls.findSum(input0)
	return result == returns



if __name__ == '__main__':
	print(example0()&example1()&example2()&example3())