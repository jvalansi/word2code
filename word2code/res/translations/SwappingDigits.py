from problem_utils import *
import copy
import string


class SwappingDigits:
    def minNumber(self, num):
        input_array = num
        N = len(num)
        
        # Given is a String num .
        # This String contains the digits of a (possibly large) positive integer.
        # For example, num ="1147" represents the integer 1147.
        # The String num will not have any leading zeros.
        # You are allowed to swap one pair of digits in the given number.
        # In other words, you may choose a pair of distinct indices i and j, and swap the characters num [i] and num [j].
        #### integers = [''.join(swap(list(num), (i, j))) for (i, j) in choose(indices(N), pair)]
        possibilities = [''.join(swap(list(num), (i, j))) for (i, j) in combinations_with_replacement(range(N), 2)]
        # Note that you may also leave the original number unchanged.
        # The new String must again describe a valid positive integer, i.e., it must not have any leading zeros.
        def valid(possibility):
            #### return (not leading(s, zeros))
            return (not startswith(possibility, 0))
        # Find and return the String that represents the smallest possible integer that can be obtained.
        #### reduce = lambda possibility: smallest(possibility)
        reduce = lambda possibility: min(possibility)
        #### return reduce(filter(possible, integers))
        return reduce(filter(valid, possibilities))

def example0():
	cls = SwappingDigits()
	input0 = "596"
	returns = "569"
	result = cls.minNumber(input0)
	return result == returns


def example1():
	cls = SwappingDigits()
	input0 = "93561"
	returns = "13569"
	result = cls.minNumber(input0)
	return result == returns


def example2():
	cls = SwappingDigits()
	input0 = "5491727514"
	returns = "1491727554"
	result = cls.minNumber(input0)
	return result == returns


def example3():
	cls = SwappingDigits()
	input0 = "10234"
	returns = "10234"
	result = cls.minNumber(input0)
	return result == returns


def example4():
	cls = SwappingDigits()
	input0 = "93218910471211292416"
	returns = "13218910471211292496"
	result = cls.minNumber(input0)
	return result == returns



if __name__ == '__main__':
	print(example0()&example1()&example2()&example3()&example4())