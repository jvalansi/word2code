from problem_utils import *

class BasketsWithApples:
	def removeExcess(self, apples):
		input_array = apples
		#  We have some baskets containing apples, and we would like to perform the following procedure in a way that maximizes the number of remaining apples.
		# First, we discard some (or none) of the baskets completely.
		# Then, if the remaining baskets do not all contain the same number of apples, we remove excess apples from the baskets until they do.
		# You will be given a int[] apples where the i-th element of apples is the number of apples in the i-th basket.
		# Return the number of apples remaining after the procedure described above is performed. 
		pass

def example0():
	cls = BasketsWithApples()
	input0 = [1, 2, 3]
	returns = 4
	result = cls.removeExcess(input0)
	return result == returns

def example1():
	cls = BasketsWithApples()
	input0 = [5, 0, 30, 14]
	returns = 30
	result = cls.removeExcess(input0)
	return result == returns

def example2():
	cls = BasketsWithApples()
	input0 = [51, 8, 38, 49]
	returns = 114
	result = cls.removeExcess(input0)
	return result == returns

def example3():
	cls = BasketsWithApples()
	input0 = [24, 92, 38, 0, 79, 45]
	returns = 158
	result = cls.removeExcess(input0)
	return result == returns

if __name__ == '__main__':
	print(example0())

