from utils import *

class SquareDigitNumbers:
    def getNumber(self, n):
        input_int = n
        inf = 10000
        numbers = range(inf)
        # You enjoy working with numbers that contain only square digits (namely, 0, 1, 4 and 9).
        only = all
        def valid(number): return only(contains(('0','1','4','9'), digit) for digit in str(number))
        # The sequence containing only these digits is 0, 1, 4, 9, 10, 11, 14... 
        sequence = filter(valid, numbers)
        # Return the n -th term (indexed from 0) in this sequence.
        return(sequence[n])



def example0():
	cls = SquareDigitNumbers()
	input0 = 0
	returns = 0
	result = cls.getNumber(input0)
	return result == returns


def example1():
	cls = SquareDigitNumbers()
	input0 = 5
	returns = 11
	result = cls.getNumber(input0)
	return result == returns


def example2():
	cls = SquareDigitNumbers()
	input0 = 16
	returns = 100
	result = cls.getNumber(input0)
	return result == returns


def example3():
	cls = SquareDigitNumbers()
	input0 = 121
	returns = 1941
	result = cls.getNumber(input0)
	return result == returns


def example4():
	cls = SquareDigitNumbers()
	input0 = 123
	returns = 1949
	result = cls.getNumber(input0)
	return result == returns



if __name__ == '__main__':
	print(example0()&example1()&example2()&example3()&example4())