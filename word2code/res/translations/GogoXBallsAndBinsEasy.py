from problem_utils import *

class GogoXBallsAndBinsEasy:
	def solve(self, T):
		input_array = T
		#  Like all other software engineers, Gogo likes to play with bins and balls.
		# He has N bins, numbered 0 through N-1.
		# Yesterday, Gogo distributed all his balls into the bins, placing S[0] balls into bin 0, S[1] balls into bin 1, and so on.
		# No two bins contained the same number of balls.
		# It is possible that one of the bins contained zero balls.
		# This morning, Gogo attended a lecture about sorting.
		# After he got home, he decided to rearrange the balls in his bins into sorted order.
		# More precisely, he wanted to reach a state with T [0] balls in bin 0, T [1] balls in bin 1, and so on, such that the following two conditions are met: T is a permutation of S T is sorted in ascending order For example, suppose that S = {2, 5, 0}, i.e., there are 2 balls in bin 0, 5 balls in bin 1, and 0 balls in bin 2.
		# Gogo would rearrange the balls to obtain T = {0, 2, 5}.
		# When rearranging the balls, Gogo always moves them one ball at a time.
		# In other words, in each move Gogo takes a single ball from one bin and places it into another bin.
		# Gogo is very smart, so he always uses the smallest possible number of moves.
		# For example, when rearranging S = {2, 5, 0} to T = {0, 2, 5}, Gogo will make exactly 5 moves.
		# One way of changing S to T in 5 moves: first Gogo will move 3 balls from bin 1 to bin 2, and then he will move 2 balls from bin 0 to bin 2.
		# You just came to visit Gogo.
		# You see that he already rearranged the balls.
		# You are given a int[] T containing the current number of balls in each of the bins.
		# You do not know the original state S. The number of balls Gogo moved depends on S. For example, we already know that for S = {2, 5, 0} Gogo would move 5 balls.
		# If he had S = {0, 5, 2} instead, he would also produce T = {0, 2, 5}, but this time he would only need 3 moves.
		# Your method must find and return the maximum number of moves Gogo could have performed.
		# In other words, among all sequences S that produce the given sequence T , find one that requires the most moves, and return that number of moves. 
		pass

def example0():
	cls = GogoXBallsAndBinsEasy()
	input0 = [0, 2, 5]
	returns = 5
	result = cls.solve(input0)
	return result == returns

def example1():
	cls = GogoXBallsAndBinsEasy()
	input0 = [5, 6, 7, 8]
	returns = 4
	result = cls.solve(input0)
	return result == returns

def example2():
	cls = GogoXBallsAndBinsEasy()
	input0 = [0, 1, 2, 10]
	returns = 11
	result = cls.solve(input0)
	return result == returns

def example3():
	cls = GogoXBallsAndBinsEasy()
	input0 = [1, 2, 3, 4, 5, 6, 7, 8]
	returns = 16
	result = cls.solve(input0)
	return result == returns

if __name__ == '__main__':
	print(example0())

