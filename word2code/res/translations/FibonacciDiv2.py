from problem_utils import *

class FibonacciDiv2:
	def find(self, N):
		input_int = N
		#  The Fibonacci sequence is defined as follows: F[0] = 0 F[1] = 1 for each i >= 2: F[i] = F[i-1] + F[i-2] Thus, the Fibonacci sequence starts as follows: 0, 1, 1, 2, 3, 5, 8, 13, ...
		# The elements of the Fibonacci sequence are called Fibonacci numbers.
		# You're given an int N .
		# You want to change N into a Fibonacci number.
		# This change will consist of zero or more steps.
		# In each step, you can either increment or decrement the number you currently have.
		# That is, in each step you can change your current number X either to X+1 or to X-1.
		# Return the smallest number of steps needed to change N into a Fibonacci number. 
		pass

def example0():
	cls = FibonacciDiv2()
	input0 = 1
	returns = 0
	result = cls.find(input0)
	return result == returns

def example1():
	cls = FibonacciDiv2()
	input0 = 13
	returns = 0
	result = cls.find(input0)
	return result == returns

def example2():
	cls = FibonacciDiv2()
	input0 = 15
	returns = 2
	result = cls.find(input0)
	return result == returns

def example3():
	cls = FibonacciDiv2()
	input0 = 19
	returns = 2
	result = cls.find(input0)
	return result == returns

def example4():
	cls = FibonacciDiv2()
	input0 = 1000000
	returns = 167960
	result = cls.find(input0)
	return result == returns

if __name__ == '__main__':
	print(example0())

