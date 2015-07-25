from problem_utils import *

class IdentifyingWood:
	def check(self, s, t):
		input_array0 = s
		input_array1 = t
		#  We call a pair of Strings ( s , t ) "wood" if t is contained in s as a subsequence.
		# (See Notes for a formal definition.)
		# Given Strings s and t , return the String "Yep, it's wood."
		# (quotes for clarity) if the pair ( s , t ) is wood and "Nope."
		# otherwise. 
		pass

def example0():
	cls = IdentifyingWood()
	input0 = "absdefgh"
	input1 = "asdf"
	returns = "Yep, it's wood."
	result = cls.check(input0, input1)
	return result == returns

def example1():
	cls = IdentifyingWood()
	input0 = "oxoxoxox"
	input1 = "ooxxoo"
	returns = "Nope."
	result = cls.check(input0, input1)
	return result == returns

def example2():
	cls = IdentifyingWood()
	input0 = "oxoxoxox"
	input1 = "xxx"
	returns = "Yep, it's wood."
	result = cls.check(input0, input1)
	return result == returns

def example3():
	cls = IdentifyingWood()
	input0 = "qwerty"
	input1 = "qwerty"
	returns = "Yep, it's wood."
	result = cls.check(input0, input1)
	return result == returns

def example4():
	cls = IdentifyingWood()
	input0 = "string"
	input1 = "longstring"
	returns = "Nope."
	result = cls.check(input0, input1)
	return result == returns

if __name__ == '__main__':
	print(example0())

