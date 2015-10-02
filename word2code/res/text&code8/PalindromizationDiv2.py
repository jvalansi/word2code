from problem_utils import *


class PalindromizationDiv2:
    def getMinimumCost(self, X):
        input_int = X
        inf = 100000
        
        
        # Little Arthur loves numbers, especially palindromic ones.
        # A palindromic string is a string that reads the same both forwards and backwards.
        def valid(possibility):
            #### possibilities = str(possibility)
            possibilities = str(possibility)
            #### reduce = lambda possibility: same(possibility, list2str(backwards(possibility)))
            reduce = (lambda possibility: eq(possibility, list2str(reversed(possibility))))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # A palindromic number is a non-negative integer such that its decimal representation (without insignificant leading zeros) is a palindromic string.
        # For example, 12321, 101, 9, and 0 are palindromic numbers but 2011, 509, and 40 are not.
        # Arthur has a number input_int and he would like to palindromize it.
        # Palindromization of a number means adding or subtracting some value to obtain a palindromic number.
        # For example, one possible way to palindromize number 25 is adding 8 resulting in number 33, which is palindromic.
        # Unfortunately Arthur cannot palindromize numbers for free.
        # The cost of palindromization in dollars is equal to the value added or subtracted.
        def mapping(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = lambda possibility: abs(subtracted(input_int, possibility))
            reduce = (lambda possibility: abs(sub(input_int, possibility)))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # In the previous example Arthur would have to pay 8 dollars.
        # Of course Arthur would like to palindromize input_int spending the least amount of money.
        # Given input_int return the minimum amount of money Arthur needs.
        #### reduce = lambda possibility: minimum(possibility)
        reduce = (lambda possibility: min(possibility))
        #### possibilities = integers(inf)
        possibilities = range(inf)
        #### return(reduce(map(mapping, filter(valid, possibilities))))
        return reduce(map(mapping, filter(valid, possibilities)))

def example0():
	cls = PalindromizationDiv2()
	input0 = 25
	returns = 3
	result = cls.getMinimumCost(input0)
	return result == returns


def example1():
	cls = PalindromizationDiv2()
	input0 = 12321
	returns = 0
	result = cls.getMinimumCost(input0)
	return result == returns


def example2():
	cls = PalindromizationDiv2()
	input0 = 40
	returns = 4
	result = cls.getMinimumCost(input0)
	return result == returns


def example3():
	cls = PalindromizationDiv2()
	input0 = 2011
	returns = 9
	result = cls.getMinimumCost(input0)
	return result == returns


def example4():
	cls = PalindromizationDiv2()
	input0 = 0
	returns = 0
	result = cls.getMinimumCost(input0)
	return result == returns



if __name__ == '__main__':
	print(example0()&example1()&example2()&example3()&example4())