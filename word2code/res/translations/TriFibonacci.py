from problem_utils import *


class TriFibonacci:
    def complete(self, A):
        input_array = A
        
        # A TriFibonacci sequence begins by defining the first three elements A[0], A[1] and A[2].
        # The remaining elements are calculated using the following recurrence: A[i] = A[i-1] + A[i-2] + A[i-3]
        def mapping(possibility):
            #### return ((A[(i - 1)] + A[(i - 2)]) + A[(i - 3)])
            return ((A[(possibility - 1)] + A[(possibility - 2)]) + A[(possibility - 3)])
        # You are given a int[] A which contains exactly one element that is equal to -1, you must replace this element with a positive number in a way that the sequence becomes a TriFibonacci sequence.
        #### number = A_(indexOf(A, -1))
        possibilities = mapping(indexOf(A, (-1)))
        # Return this number.
        #### return number
        return possibilities
        # If no such positive number exists, return -1.
        # 

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