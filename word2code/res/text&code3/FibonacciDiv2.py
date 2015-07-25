from problem_utils import *

class FibonacciDiv2:
	def find(self, N):
		input_int = N
		# The Fibonacci sequence is defined as follows:
		
		# F[0] = 0
		# F[1] = 1
		# for each i >= 2: F[i] = F[i-1] + F[i-2]
		F = {0:0,1:1}
		for i in range(2,input_int):
			F[i] = F[i-1] + F[i-2]
		# Thus, the Fibonacci sequence starts as follows: 0, 1, 1, 2, 3, 5, 8, 13, ...
		# The elements of the Fibonacci sequence are called Fibonacci numbers.
		
		# You're given an int N.
		# You want to change N into a Fibonacci number.
		# This change will consist of zero or more steps.
		# In each step, you can either increment or decrement the number you currently have.
		# That is, in each step you can change your current number X either to X+1 or to X-1.
		elements = [+1,-1]
		possibilities = []
		for i in range(N+1):
			possibilities.extend(product(elements, repeat = i))
		valid = lambda possibility: input_int + sum(possibility) in F.values()

		# Return the smallest number of steps needed to change N into a Fibonacci number.
		#### return (smallest(number(steps) for steps in possibilities if valid(steps)))
		return (min(len(possibility) for possibility in possibilities if valid(possibility)))
			
if __name__ == '__main__':
	N = 	10
	fd2 = FibonacciDiv2()
	print(fd2.find(N))