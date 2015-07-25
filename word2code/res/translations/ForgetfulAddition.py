from problem_utils import *

class ForgetfulAddition:
	def minNumber(self, expression):
		input_array = expression
		#  Alice had two positive integers, a and b.
		# She typed the expression "a+b" into her computer, but the '+' key malfunctioned.
		# For example, instead of "128+9" the computer's screen now shows "1289".
		# Later, Bob saw the string on the screen.
		# He knows that the '+' sign is missing but he does not know where it belongs.
		# He now wonders what is the smallest possible result of Alice's original expression.
		# For example, if Bob sees the string "1289", Alice's expression is either "128+9" or "12+89" or "1+289".
		# These expressions evaluate to 137, 101, and 290.
		# The smallest of those three results is 101.
		# You are given a String expression that contains the expression on Alice's screen.
		# Compute and return the smallest possible result after inserting the missing plus sign 
		pass

def example0():
	cls = ForgetfulAddition()
	input0 = "22"
	returns = 4
	result = cls.minNumber(input0)
	return result == returns

def example1():
	cls = ForgetfulAddition()
	input0 = "123"
	returns = 15
	result = cls.minNumber(input0)
	return result == returns

def example2():
	cls = ForgetfulAddition()
	input0 = "1289"
	returns = 101
	result = cls.minNumber(input0)
	return result == returns

def example3():
	cls = ForgetfulAddition()
	input0 = "31415926"
	returns = 9067
	result = cls.minNumber(input0)
	return result == returns

def example4():
	cls = ForgetfulAddition()
	input0 = "98765"
	returns = 863
	result = cls.minNumber(input0)
	return result == returns

if __name__ == '__main__':
	print(example0())

