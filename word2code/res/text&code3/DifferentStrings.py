from problem_utils import *
from operator import *
from string import lowercase

class DifferentStrings:
	def minimize(self, A, B):
		input_array1 = A
		input_array2 = B
		N = min(len(input_array1),len(input_array2))
		elements = lowercase

		# If X and Y are two Strings of equal length N, then the difference between them is defined as the number of indices i where the i-th character of X and the i-th character of Y are different.
		#### difference = lambda X: number(different(X[i], Y[i]) for i in indices(N))
		mapping = lambda possibility: len(ne(possibility[i], input_array1[i]) for i in range(N))
		
		# For example, the difference between the words "ant" and "art" is 1.
		
		# You are given two Strings, A and B, where the length of A is less than or equal to the length of B.  
		# You can apply an arbitrary number of operations to A, where each operation is one of the following:
		#	Choose a character c and add it to the beginning of A.
		#	Choose a character c and add it to the end of A.
		possibilities = csubsets(input_array2, N)
		
		# Apply the operations in such a way that A and B have the same length and the difference between them is as small as possible.
		# Return this minimum possible difference.
		#### return(minimum([difference(possibility) for possibility in possibilities]))
		return(min([mapping(possibility) for possibility in possibilities]))
			
if __name__ == '__main__':
	A = "koder"
	B = "topcoder"
	ds = DifferentStrings()
	print(ds.minimize(A, B))