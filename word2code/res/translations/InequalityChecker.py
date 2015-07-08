from utils import *

class InequalityChecker:
	def getDifferences(self, n):
		input_int = n
		#  Using mathematical induction it is possible to prove the following inequality when n >1: s = 13 + 23 + ... + (n-1)3 < n4/4 < 13 + 23 + ... + n3 = S Given n return (S+s)/2 - n 4 /4 as a int[] with 2 elements.
		# Elements 0 and 1 denote the numerator and denominator of the return value, respectively, when written in least terms (reduced). 
		pass

def example0():
	cls = InequalityChecker()
	input0 = 2
	returns = [ 1, 1 ]
	result = cls.getDifferences(input0)
	return result == returns

def example1():
	cls = InequalityChecker()
	input0 = 3
	returns = [ 9, 4 ]
	result = cls.getDifferences(input0)
	return result == returns

def example2():
	cls = InequalityChecker()
	input0 = 100
	returns = [ 2500, 1 ]
	result = cls.getDifferences(input0)
	return result == returns

if __name__ == '__main__':
	print(example0())

