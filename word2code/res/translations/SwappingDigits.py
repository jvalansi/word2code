from utils import *
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
        choose = combinations_with_replacement
        pair = 2
        indices = range
        integers = [''.join(swap(list(num), (i,j))) for i,j in choose(indices(N), pair)]
        # Note that you may also leave the original number unchanged.
        # The new String must again describe a valid positive integer, i.e., it must not have any leading zeros.
        zeros = 0
        leading = startswith
        def valid(s): return not(leading(s, zeros)) 
        # Find and return the String that represents the smallest possible integer that can be obtained.
        # ROOT-0(root=Find-1(conj_and=return-3(dobj=String-5(det=the-4, rcmod=represents-7(nsubj=that-6, dobj=integer-11(det=the-8, amod=smallest-9, amod=possible-10, rcmod=obtained-15(nsubjpass=that-12, aux=can-13, auxpass=be-14)))))))
        smallest = min
        possible = valid
        return(smallest(filter(possible, integers)))



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