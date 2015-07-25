from problem_utils import *

class CheckFunction:
	def newFunction(self, code):
		input_array = code
		#  You are given a String code containing a message composed entirely of decimal digits ('0'-'9').
		# Each digit consists of some number of dashes (see diagram below).
		# A "check function" of a message is defined as the total number of dashes in the message.
		def check_function(message):
			total = lambda possibility: sum(possibility)
			number = lambda arg0, arg1: countOf(arg1, arg0)
			dashes = '-'
			return(total(number(dashes,message))) 
		# Return the value of the check function for the message represented in code .
		return(check_function(code)) 

def example0():
	cls = CheckFunction()
	input0 = "13579"
	returns = 21
	result = cls.newFunction(input0)
	return result == returns

def example1():
	cls = CheckFunction()
	input0 = "02468"
	returns = 28
	result = cls.newFunction(input0)
	return result == returns

def example2():
	cls = CheckFunction()
	input0 = "73254370932875002027963295052175"
	returns = 157
	result = cls.newFunction(input0)
	return result == returns

if __name__ == '__main__':
	print(example0())

