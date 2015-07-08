from utils import *

class TheEquation:
    def leastSum(self, X, Y, P):
        input_int0 = X
        input_int1 = Y
        input_int2 = P
        # You are given three positive integers, X , Y and P .
        # Return the least sum of two positive integers a and b such that P is a divisor of a* X +b* Y .
        # ROOT-0(root=Return-1(dep=sum-4(det=the-2, amod=least-3, prep_of=integers-8(num=two-6, amod=positive-7)), rcmod=divisor-17(nsubj=a-9(conj_and=b-11, dep=such-12, prep_that=P-14), cop=is-15, det=a-16, prep_of=X-21(det=a-19, nn=*-20, conj_+=b-23), dep=Y-25(dep=*-24))))
        least = min
        divisor = is_divisor
        return(least(sum((a,b)) for a,b in product(range(1,P),repeat=2) if divisor(P,a*X+b*Y)))



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