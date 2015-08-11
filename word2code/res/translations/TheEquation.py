from problem_utils import *


class TheEquation:
    def leastSum(self, X, Y, P):
        input_int0 = X
        input_int1 = Y
        input_int2 = P
        
        # You are given three positive integers, X , Y and P .
        # Return the least sum of two positive integers a and b such that P is a divisor of a* X +b* Y .
        #### reduce = lambda possibility: least(possibility)
        reduce = (lambda possibility: min(possibility))
        #### mapping = lambda (a, b): sum((a, b))
        mapping = (lambda (a, b): sum((a, b)))
        #### possibilities = product(range(1, P), repeat=2)
        possibilities = product(range(1, P), repeat=2)
        #### valid = lambda (a, b): divisor(P, ((a * X) + (b * Y)))
        valid = (lambda (a, b): is_divisor(P, ((a * X) + (b * Y))))
        #### return(reduce(map(mapping, filter(valid, possibilities))))
        return reduce(map(mapping, filter(valid, possibilities)))

def example0():
	cls = TheEquation()
	input0 = 2
	input1 = 6
	input2 = 5
	returns = 3
	result = cls.leastSum(input0, input1, input2)
	return result == returns


def example1():
	cls = TheEquation()
	input0 = 5
	input1 = 5
	input2 = 5
	returns = 2
	result = cls.leastSum(input0, input1, input2)
	return result == returns


def example2():
	cls = TheEquation()
	input0 = 998
	input1 = 999
	input2 = 1000
	returns = 501
	result = cls.leastSum(input0, input1, input2)
	return result == returns


def example3():
	cls = TheEquation()
	input0 = 1
	input1 = 1
	input2 = 1000
	returns = 1000
	result = cls.leastSum(input0, input1, input2)
	return result == returns


def example4():
	cls = TheEquation()
	input0 = 347
	input1 = 873
	input2 = 1000
	returns = 34
	result = cls.leastSum(input0, input1, input2)
	return result == returns



if __name__ == '__main__':
	print(example0()&example1()&example2()&example3()&example4())