from utils import *

class EqualSubstrings:
	def getSubstrings(self, str):
		input_array = str
		#  You will be given a String str consisting of lowercase letters.
		# You will return a String[] containing elements x and y in that order.
		# The returned Strings x and y must satisfy: 1) The string xy (x with y concatenated on the end) must equal str .
		# 2) The number of a's in x must equal the number of b's in y.
		# 3) If multiple solutions are possible, use the one that maximizes the length of x.
		# See the examples for further clarifications. 
		pass

def example0():
	cls = EqualSubstrings()
	input0 = "aaabbb"
	returns = [ "aaa", "bbb" ]
	result = cls.getSubstrings(input0)
	return result == returns

def example1():
	cls = EqualSubstrings()
	input0 = "bbbaaa"
	returns = [ "bbb", "aaa" ]
	result = cls.getSubstrings(input0)
	return result == returns

def example2():
	cls = EqualSubstrings()
	input0 = "bbbbbb"
	returns = [ "bbbbbb", "" ]
	result = cls.getSubstrings(input0)
	return result == returns

def example3():
	cls = EqualSubstrings()
	input0 = "aaaaaa"
	returns = [ "", "aaaaaa" ]
	result = cls.getSubstrings(input0)
	return result == returns

def example4():
	cls = EqualSubstrings()
	input0 = "abjlkbjalkbjaljsbljbalb"
	returns = [ "abjlkbjalkbjaljs", "bljbalb" ]
	result = cls.getSubstrings(input0)
	return result == returns

if __name__ == '__main__':
	print(example0())

