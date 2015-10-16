from problem_utils import *


class WinterAndMandarins:
    def getNumber(self, bags, K):
        input_array = bags
        input_int = K
        
        
        
        # It's winter time!
        # Time to eat a lot of mandarins with your friends.
        # You have several input_array with mandarins.
        # You are given an int[] input_array .
        # For each i, the i-th element of input_array represents the number of mandarins in the i-th bag.
        # You are also given an int input_int .
        # You want to choose exactly input_int input_array and distribute them among you and your friends.
        #### chosen = choose(input_array, input_int)
        possibilities = subsets(input_array, input_int)
        # To be as fair as possible, you want to minimize the difference between the chosen bag with most mandarins and the chosen bag with fewest mandarins.
        def mapping0(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = lambda possibility: difference(most(possibility), fewest(possibility))
            reduce = (lambda possibility: sub(max(possibility), min(possibility)))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # Return the smallest difference that can be achieved.
        #### def reduce(possibility): return smallest(possibility)
        def reduce(possibility): return min(possibility)
        #### return reduce(map(mapping0, chosen))
        return reduce(map(mapping0, possibilities))

def example0():
	cls = WinterAndMandarins()
	input0 = [10, 20, 30]
	input1 = 2
	returns = 10
	result = cls.getNumber(input0, input1)
	return result == returns


def example1():
	cls = WinterAndMandarins()
	input0 = [4, 7, 4]
	input1 = 3
	returns = 3
	result = cls.getNumber(input0, input1)
	return result == returns


def example2():
	cls = WinterAndMandarins()
	input0 = [4, 1, 2, 3]
	input1 = 3
	returns = 2
	result = cls.getNumber(input0, input1)
	return result == returns


def example3():
	cls = WinterAndMandarins()
	input0 = [5, 4, 6, 1, 9, 4, 2, 7, 5, 6]
	input1 = 4
	returns = 1
	result = cls.getNumber(input0, input1)
	return result == returns


def example4():
	cls = WinterAndMandarins()
	input0 = [47, 1000000000, 1, 74]
	input1 = 2
	returns = 27
	result = cls.getNumber(input0, input1)
	return result == returns



if __name__ == '__main__':
	print(example0()&example1()&example2()&example3()&example4())