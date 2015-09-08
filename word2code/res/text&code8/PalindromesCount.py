from problem_utils import *


class PalindromesCount:
    def count(self, A, B):
        A = list(A)
        B = list(B)
        input_array0 = A
        input_array1 = B
        N0 = len(A)
        
        
        # input_array0 palindrome is a string that is the same whether it is read from left to right or from right to left.
        def valid0(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = lambda possibility: same(string, string[::(-1)])
            reduce = (lambda possibility: eq(possibility, possibility[::(-1)]))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # Little Dazdraperma likes palindromes a lot.
        # As a birthday gift she received two strings input_array0 and input_array1 .
        # Now she is curious if there is a way to insert string input_array1 into string input_array0 so that the resulting string is a palindrome.
        def mapping0(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = lambda possibility: insert(input_array0, possibility, input_array1)
            reduce = (lambda possibility: insert(input_array0, possibility, input_array1))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # You agreed to help her and even tell how many different variants of such insertions exist.
        # Two variants are considered different if string input_array1 is inserted in different places.
        #### variants = range(inclusive(N0))
        possibilities = range(inclusive(N0))
        # Return the number of possible insertion variants.
        #### def reduce(possibility): return number(possibility)
        def reduce(possibility): return len(possibility)
        #### return reduce(filter(possible, map(insertion, variants)))
        return reduce(filter(valid0, map(mapping0, possibilities)))
        # For example, let input_array0 ="aba" and input_array1 ="b".
        # You can insert input_array1 in 4 different places: Before the first letter of input_array0 .
        # The result is "baba" and it is not a palindrome.
        # After the first letter 'a'.
        # The result is "abba" and it is a palindrome.
        # After the letter 'b'.
        # The result is "abba" and it is also a palindrome.
        # After the second letter 'a'.
        # The result is "abab" and it is not a palindrome.
        # So, the answer for this example is 2.
        #### pass
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