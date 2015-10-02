from problem_utils import *
from operator import *
from string import lowercase


class DifferentStrings:
    def minimize(self, A, B):
        input_array1 = A
        input_array2 = B
        N = len(input_array1)
        M = len(input_array2)
        elements = lowercase
        
        
        
        # If X and Y are two Strings of equal length N, then the difference between them is defined as the number of indices i where the i-th character of X and the i-th character of Y are different.
        # For example, the difference between the words "ant" and "art" is 1.
        # You are given two Strings, input_array1 and input_array2, where the length of input_array1 is less than or equal to the length of input_array2.
        # You can apply an arbitrary number of operations to input_array1, where each operation is one of the following:
        # Choose a character c and add it to the beginning of input_array1.
        # Choose a character c and add it to the end of input_array1.
        # Apply the operations in such a way that input_array1 and input_array2 have the same length and the difference between them is as small as possible.
        # Return this minimum possible difference.
        #### def mapping(possibility): return len(difference(possibility, input_array1))
        def mapping(possibility): return len(diff(possibility, input_array1))
        #### possibilities = csubsets(input_array2, N)
        possibilities = csubsets(input_array2, N)
        #### def reduce(possibility): return minimum(possibility)
        def reduce(possibility): return min(possibility)
        #### return reduce(map(difference, possibilities))
        return reduce(map(mapping, possibilities))

def example0():
	A = "koder"
	B = "topcoder"
	ds = DifferentStrings()
	result = ds.minimize(A, B)
	returns = 1
	return result == returns
    
if __name__ == '__main__':
    print(example0())