from utils import *

class PalindromesCount:
	def count(self, A, B):
		A = list(A)
		B = list(B)
		input_array0 = A
		input_array1 = B
		N0 = len(A)
		#  A palindrome is a string that is the same whether it is read from left to right or from right to left.
		same = eq
		palindrome = lambda string: same(string, string[::-1])
		# Little Dazdraperma likes palindromes a lot.
		# As a birthday gift she received two strings A and B .
		# Now she is curious if there is a way to insert string B into string A so that the resulting string is a palindrome.
		insert = lambda possibility: A[:possibility] + B + A[possibility:]
		# You agreed to help her and even tell how many different variants of such insertions exist.
		# Two variants are considered different if string B is inserted in different places.
		variants = range(inclusive(N0))
		# Return the number of possible insertion variants.
		number = len
		possible = palindrome
		insertion = insert
		return(number(filter(possible, map(insertion, variants))))
		# For example, let A ="aba" and B ="b".
		# You can insert B in 4 different places: Before the first letter of A .
		# The result is "baba" and it is not a palindrome.
		# After the first letter 'a'.
		# The result is "abba" and it is a palindrome.
		# After the letter 'b'.
		# The result is "abba" and it is also a palindrome.
		# After the second letter 'a'.
		# The result is "abab" and it is not a palindrome.
		# So, the answer for this example is 2. 
		pass

def example0():
	cls = PalindromesCount()
	input0 = "aba"
	input1 = "b"
	returns = 2
	result = cls.count(input0, input1)
	return result == returns

def example1():
	cls = PalindromesCount()
	input0 = "aa"
	input1 = "a"
	returns = 3
	result = cls.count(input0, input1)
	return result == returns

def example2():
	cls = PalindromesCount()
	input0 = "aca"
	input1 = "bb"
	returns = 0
	result = cls.count(input0, input1)
	return result == returns

def example3():
	cls = PalindromesCount()
	input0 = "abba"
	input1 = "abba"
	returns = 3
	result = cls.count(input0, input1)
	return result == returns

def example4():
	cls = PalindromesCount()
	input0 = "topcoder"
	input1 = "coder"
	returns = 0
	result = cls.count(input0, input1)
	return result == returns

if __name__ == '__main__':
	print(example0()&example1()&example2()&example3())

