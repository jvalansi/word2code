from utils import *

class InfiniteString:
	def equal(self, s, t):
		input_array0 = s
		input_array1 = t
		inf = 1000
		#  Given a string s, let f(s) denote the infinite string obtained by concatenating infinitely many copies of s. For example, if s = "abc" then f(s) = "abcabcabcabc...".
		def f(s): return(s*inf)[:inf]
		# Note that the string f(s) still has a beginning.
		# Hence, f("abc") and f("bca") are two different infinite strings: the first one starts with an 'a' while the other starts with a 'b'.
		# Sometimes, two different finite strings can produce the same infinite string.
		# For example, f("abc") is the same as f("abcabc").
		# You are given Strings s and t .
		# Check whether f( s ) equals f( t ).
		# If the two infinite strings are equal, return "Equal".
		equal = eq
		return "Equal" if equal(f(s),f(t)) else "Not equal" 
		# Otherwise, return "Not equal". 

def example0():
	cls = InfiniteString()
	input0 = "ab"
	input1 = "abab"
	returns = "Equal"
	result = cls.equal(input0, input1)
	return result == returns

def example1():
	cls = InfiniteString()
	input0 = "abc"
	input1 = "bca"
	returns = "Not equal"
	result = cls.equal(input0, input1)
	return result == returns

def example2():
	cls = InfiniteString()
	input0 = "abab"
	input1 = "aba"
	returns = "Not equal"
	result = cls.equal(input0, input1)
	return result == returns

def example3():
	cls = InfiniteString()
	input0 = "aaaaa"
	input1 = "aaaaaa"
	returns = "Equal"
	result = cls.equal(input0, input1)
	return result == returns

def example4():
	cls = InfiniteString()
	input0 = "ababab"
	input1 = "abab"
	returns = "Equal"
	result = cls.equal(input0, input1)
	return result == returns

def example5():
	cls = InfiniteString()
	input0 = "a"
	input1 = "z"
	returns = "Not equal"
	result = cls.equal(input0, input1)
	return result == returns

if __name__ == '__main__':
	print(example0())

