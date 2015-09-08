from problem_utils import *


class TriFibonacci:
    def complete(self, A):
        input_array = A
        
        
        # input_array TriFibonacci sequence begins by defining the first three elements input_array[0], input_array[1] and input_array[2].
        # The remaining elements are calculated using the following recurrence: input_array[i] = input_array[i-1] + input_array[i-2] + input_array[i-3]
        def mapping0(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = lambda possibility: ((input_array[(i - 1)] + input_array[(i - 2)]) + input_array[(i - 3)])
            reduce = (lambda possibility: ((input_array[(possibility - 1)] + input_array[(possibility - 2)]) + input_array[(possibility - 3)]))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # You are given a int[] input_array which contains exactly one element that is equal to -1, you must replace this element with a positive number in a way that the sequence becomes a TriFibonacci sequence.
        #### number = A_(indexOf(A, -1))
        possibilities = mapping0(indexOf(A, (-1)))
        # Return this number.
        #### reduce = lambda possibility: number
        reduce = (lambda possibility: possibilities)
        #### return(reduce(possibilities))
        return reduce(possibilities)
        # If no such positive number exists, return -1.

def example0():
	cls = TriFibonacci()
	input0 = [1,2,3,-1]
	returns = 6
	result = cls.complete(input0)
	return result == returns


def example1():
	cls = TriFibonacci()
	input0 = [10, 20, 30, 60, -1 , 200]
	returns = 110
	result = cls.complete(input0)
	return result == returns


def example2():
	cls = TriFibonacci()
	input0 = [1, 2, 3, 5, -1]
	returns = -1
	result = cls.complete(input0)
	return result == returns


def example3():
	cls = TriFibonacci()
	input0 = [1, 1, -1, 2, 3]
	returns = -1
	result = cls.complete(input0)
	return result == returns


def example4():
	cls = TriFibonacci()
	input0 = [-1, 7, 8, 1000000]
	returns = 999985
	result = cls.complete(input0)
	return result == returns



if __name__ == '__main__':
	print(example0())