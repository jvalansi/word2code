from problem_utils import *

class LittleElephantAndBooks:
	def getNumber(self, pages, number):
		input_array = pages
		input_int = number
		#  Little Elephant from the Zoo of Lviv has a bunch of books.
		# You are given a int[] pages .
		# Each element of pages is the number of pages in one of those books.
		# There are no two books with the same number of pages.
		# You are also given a int number .
		# As a homework from the teacher, Little Elephant must read exactly number of his books during the summer.
		# (Little Elephant has strictly more than number books.)
		# All other elephants in the school also got the exact same homework.
		# Little Elephant knows that the other elephants are lazy: they will simply pick the shortest number books, so that they have to read the smallest possible total number of pages.
		# Little Elephant wants to be a good student and read a bit more than the other elephants.
		# He wants to pick the subset of books with the second smallest number of pages.
		# In other words, he wants to pick a subset of books with the following properties: There are exactly number books in the chosen subset.
		# The total number of pages of those books is greater than the smallest possible total number of pages.
		# The total number of pages of those books is as small as possible (given the above conditions).
		# Return the total number of pages Little Elephant will have to read. 
		pass

def example0():
	cls = LittleElephantAndBooks()
	input0 = [1, 2]
	input1 = 1
	returns = 2
	result = cls.getNumber(input0, input1)
	return result == returns

def example1():
	cls = LittleElephantAndBooks()
	input0 = [74, 7, 4, 47, 44]
	input1 = 3
	returns = 58
	result = cls.getNumber(input0, input1)
	return result == returns

def example2():
	cls = LittleElephantAndBooks()
	input0 = [3, 1, 9, 7, 2, 8, 6, 4, 5]
	input1 = 7
	returns = 29
	result = cls.getNumber(input0, input1)
	return result == returns

def example3():
	cls = LittleElephantAndBooks()
	input0 = [74, 86, 32, 13, 100, 67, 77]
	input1 = 2
	returns = 80
	result = cls.getNumber(input0, input1)
	return result == returns

if __name__ == '__main__':
	print(example0())

