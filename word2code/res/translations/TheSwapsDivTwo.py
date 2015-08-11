from problem_utils import *
import copy


class TheSwapsDivTwo:
    def find(self, sequence):
        input_array = sequence
        N = len(sequence)
        
        # John has a sequence of integers.
        # Brus is going to choose two different positions in John's sequence and swap the elements at those positions.
        #### possibilities = choose(positions(N), two)
        possibilities = combinations(range(N), 2)
        # (The two swapped elements may have the same value.)
        # Return the number of different sequences Brus can obtain after he makes the swap.
        #### return number(different(sequences))
        return len(set((tuple(swap(sequence, p)) for p in possibilities)))

def example0():
	cls = TheSwapsDivTwo()
	input0 = [4, 7, 4]
	returns = 3
	result = cls.find(input0)
	return result == returns


def example1():
	cls = TheSwapsDivTwo()
	input0 = [1, 47]
	returns = 1
	result = cls.find(input0)
	return result == returns


def example2():
	cls = TheSwapsDivTwo()
	input0 = [9, 9, 9, 9]
	returns = 1
	result = cls.find(input0)
	return result == returns


def example3():
    cls = TheSwapsDivTwo()
    input0 = [22, 16, 36, 35, 14, 9, 33, 6, 28, 12, 18, 14, 47, 46, 29, 22, 14, 17, 4, 15, 28, 6, 39, 24, 47, 37]
    returns = 319
    result = cls.find(input0);
    return result == returns



if __name__ == '__main__':
	print(example0()&example1()&example2()&example3())