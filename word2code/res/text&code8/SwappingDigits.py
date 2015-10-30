from problem_utils import *
import copy
import string


class SwappingDigits:
    def minNumber(self, num):
        input_array = num
        N = len(num)
        
        
        
        # Given is a String input_array .
        # This String contains the digits of a (possibly large) positive integer.
        # For example, input_array ="1147" represents the integer 1147.
        # The String input_array will not have any leading zeros.
        # You are allowed to swap one pair of digits in the given number.
        # In other words, you may choose a pair of distinct indices i and j, and swap the characters input_array [i] and input_array [j].z
        #### possibilities = choose(indices(N), pair)
        possibilities = combinations_with_replacement(range(N), 2)
        #### integers = (lambda possibility: list2str(swap(list(input_array), possibility))
        mapping0 = (lambda possibility: list2str(swap(list(input_array), possibility)))
        # Note that you may also leave the original number unchanged.
        # The new String must again describe a valid positive integer, i.e., it must not have any leading zeros.
        def valid0(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = lambda possibility: (not(leading(s, zeros)))
            reduce = (lambda possibility: (not_(startswith(possibility, 0))))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # Find and return the String that represents the smallest possible integer that can be obtained.
        #### def reduce(possibility): return smallest(possibility)
        def reduce(possibility): return min(possibility)
        #### return reduce(filter(possible, integers))
        return reduce(filter(valid0, map(mapping0, possibilities)))

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