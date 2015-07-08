from utils import *

class SumOfPower:
    def findSum(self, array):
        input_array = array
        # You are given a int[] array .
        # At any moment, you may choose a nonempty contiguous subsequence of array .
        coniguous_subsequence = csubsets
        possibilities = coniguous_subsequence(array)
        # Whenever you do so, you will gain power equal to the sum of all elements in the chosen subsequence.
        def power(subsequence): return sum(subsequence) 
        # You chose each possible contiguous subsequence exactly once, each time gaining some power.
        # Compute and return the total amount of power you gained.
        # ROOT-0(root=gained-10(dep=Compute-1(conj_and=return-3(dobj=amount-6(det=the-4, amod=total-5, prep_of=power-8))), nsubj=you-9))
        total = sum
        return(total(map(power, possibilities)))



def example0():
	cls = SumOfPower()
	input0 = [1,2]
	returns = 6
	result = cls.findSum(input0)
	return result == returns


def example1():
	cls = SumOfPower()
	input0 = [1,1,1]
	returns = 10
	result = cls.findSum(input0)
	return result == returns


def example2():
	cls = SumOfPower()
	input0 = [3,14,15,92,65]
	returns = 1323
	result = cls.findSum(input0)
	return result == returns


def example3():
	cls = SumOfPower()
	input0 = [1,2,3,4,5,6,7,8,9,10]
	returns = 1210
	result = cls.findSum(input0)
	return result == returns



if __name__ == '__main__':
	print(example0()&example1()&example2()&example3())