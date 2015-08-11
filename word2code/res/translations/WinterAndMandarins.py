from problem_utils import *


class WinterAndMandarins:
    def getNumber(self, bags, K):
        input_array = bags
        input_int = K
        
        # It's winter time!
        # Time to eat a lot of mandarins with your friends.
        # You have several bags with mandarins.
        # You are given an int[] bags .
        # For each i, the i-th element of bags represents the number of mandarins in the i-th bag.
        # You are also given an int K .
        # You want to choose exactly K bags and distribute them among you and your friends.
        #### chosen = choose(bags, K)
        possibilities = subsets(bags, K)
        # To be as fair as possible, you want to minimize the difference between the chosen bag with most mandarins and the chosen bag with fewest mandarins.
        def mapping(possibility):
            #### return difference(most(possibility), fewest(possibility))
            return sub(max(possibility), min(possibility))
        # Return the smallest difference that can be achieved.
        #### return smallest(map(mapping, chosen))
        return min(map(mapping, possibilities))

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