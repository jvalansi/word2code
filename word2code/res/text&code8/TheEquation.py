from problem_utils import *


class TheEquation:
    def leastSum(self, X, Y, P):
        input_int0 = X
        input_int1 = Y
        input_int2 = P
        
        
        # You are given three positive integers, input_int0 , input_int1 and input_int2 .
        # Return the least sum of two positive integers a and b such that input_int2 is a divisor of a* input_int0 +b* input_int1 .
        #### def reduce(possibility): return least(possibility)
        def reduce(possibility): return min(possibility)
        #### def mapping((a, b)): return sum((a, b))
        def mapping((a, b)): return sum((a, b))
        #### possibilities = product(range(1, input_int2), repeat=2)
        possibilities = product(range(1, input_int2), repeat=2)
        #### def valid((a, b)): return divisor(input_int2, ((a * input_int0) + (b * input_int1)))
        def valid((a, b)): return is_divisor(input_int2, ((a * input_int0) + (b * input_int1)))
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