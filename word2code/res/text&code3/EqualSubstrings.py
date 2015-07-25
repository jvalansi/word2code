from problem_utils import *
from operator import *
from string import lowercase

class EqualSubstrings:
	def getSubstrings(self, str):
		input_array = str
		types = lowercase
		# You will be given a String str consisting of lowercase letters.  
		# You will return a String[] containing elements x and y in that order.
		
		# The returned Strings x and y must satisfy:
		#	1) The string xy (x with y concatenated on the end) must equal str.
		#### valid = lambda x, y: equal(concatenated(x, y), str)
		valid1 = lambda possibility0, possibility1: eq(add(possibility0, possibility1), input_array)

		#	2) The number of a's in x must equal the number of b's in y.
		#### valid = lambda x, y: equal(number(x, a[0]),number(y, b[0]))
		valid2 = lambda possibility0, possibility1: eq(countOf(possibility0, types[0]), countOf(possibility1, types[0]))

		#	3) If multiple solutions are possible, use the one that maximizes the length of x.
			
		# 	See the examples for further clarifications.
		return max([x,y] for x in csubsets(str) for y in csubsets(str) if valid1(x,y) and valid2(x,y))   
		

if __name__ == '__main__':
	str = 'aaabbb'
	es = EqualSubstrings()
	print(es.getSubstrings(str))