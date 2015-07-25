from problem_utils import *

class FoxAndGame:
	def countStars(self, result):
		input_array = result
		#  Fox Ciel is playing the popular game 'Cut the Rope' on her smartphone.
		# The game has multiple stages, and for each stage the player can gain between 0 and 3 stars, inclusive.
		# You are given a String[] result containing Fox Ciel's current results: For each stage, result contains an element that specifies Ciel's result in that stage.
		# More precisely, result [i] will be "---" if she got 0 stars in stage i, "o--" if she got 1 star, "oo-" if she got 2 stars and "ooo" if she managed to get all 3 stars.
		# Return the total number of stars Ciel has at the moment. 
		pass

def example0():
	cls = FoxAndGame()
	input0 = ["ooo", "ooo"]
	returns = 6
	result = cls.countStars(input0)
	return result == returns

def example1():
	cls = FoxAndGame()
	input0 = ["ooo", "oo-", "o--"]
	returns = 6
	result = cls.countStars(input0)
	return result == returns

def example2():
	cls = FoxAndGame()
	input0 = ["ooo", "---", "oo-", "---", "o--"]
	returns = 6
	result = cls.countStars(input0)
	return result == returns

def example3():
	cls = FoxAndGame()
	input0 = ["o--", "o--", "o--", "ooo", "---"]
	returns = 6
	result = cls.countStars(input0)
	return result == returns

def example4():
	cls = FoxAndGame()
	input0 = ["---", "o--", "oo-", "ooo", "ooo", "oo-", "o--", "---"]
	returns = 12
	result = cls.countStars(input0)
	return result == returns

def example5():
	cls = FoxAndGame()
	input0 = ["---", "---", "---", "---", "---", "---"]
	returns = 0
	result = cls.countStars(input0)
	return result == returns

def example6():
	cls = FoxAndGame()
	input0 = ["oo-"]
	returns = 2
	result = cls.countStars(input0)
	return result == returns

if __name__ == '__main__':
	print(example0())

