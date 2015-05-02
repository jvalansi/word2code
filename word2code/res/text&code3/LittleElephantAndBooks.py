from utils import *
from operator import *

class LittleElephantAndBooks:
	def getNumber(self, pages, number):
		input_array = pages
		input_int = number
		# Little Elephant from the Zoo of Lviv has a bunch of books.
		# You are given a int[] pages.
		# Each element of pages is the number of pages in one of those books.
		# There are no two books with the same number of pages.
		possibilities = subsets(input_array)
		
		# You are also given a int number.
		# As a homework from the teacher, Little Elephant must read exactly number of his books during the summer.
		# (Little Elephant has strictly more than number books.)
		
		# All other elephants in the school also got the exact same homework.
		# Little Elephant knows that the other elephants are lazy: 
		# they will simply pick the shortest number books, so that they have to read the smallest possible total number of pages.
		# Little Elephant wants to be a good student and read a bit more than the other elephants.
		# He wants to pick the subset of books with the second smallest number of pages.
		# In other words, he wants to pick a subset of books with the following properties:
		
		
		# There are exactly number books in the chosen subset.
		#### valid1 = lambda subset:	exactly(len(subset), number)
		valid1 = lambda possibility:	eq(len(possibility), input_int)

		# The total number of pages of those books is greater than the smallest possible total number of pages.
		#### valid2 = lambda possibility:	greater(total(pages), smallest(total(pages) for pages in possibilities if valid1(pages)))
		valid2 = lambda possibility:	gt(sum(possibility), min(sum(possibility) for possibility in possibilities if valid1(possibility)))
		
		# The total number of pages of those books is as small as possible (given the above conditions).
			
		# Return the total number of pages Little Elephant will have to read.
		#### return(min(total(pages) for pages in possibilities if valid1(pages) and valid2(pages)))
		return(min(sum(possibility) for possibility in possibilities if valid1(possibility) and valid2(possibility)))
	
if __name__ == '__main__':
	pages = [1, 2]
	number = 1
	leab = LittleElephantAndBooks()
	print(leab.getNumber(pages, number)) 