from problem_utils import *


class InfiniteString:
    def equal(self, s, t):
        input_array0 = s
        input_array1 = t
        inf = 1000
        
        
        # Given a string input_array0, let f(input_array0) denote the infinite string obtained by concatenating infinitely many copies of input_array0. For example, if input_array0 = "abc" then f(input_array0) = "abcabcabcabc...".
        def mapping0(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = lambda possibility: getitem(copies(possibility, infinitely), slice(0,inf))
            reduce = (lambda possibility: getitem(mul(possibility, inf), slice(0,inf)))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # Note that the string f(input_array0) still has a beginning.
        # Hence, f("abc") and f("bca") are two different infinite strings: the first one starts with an 'a' while the other starts with a 'b'.
        # Sometimes, two different finite strings can produce the same infinite string.
        # For example, f("abc") is the same as f("abcabc").
        # You are given Strings input_array0 and input_array1 .
        # Check whether f( input_array0 ) equals f( input_array1 ).
        # If the two infinite strings are equal, return "Equal".
        #### possibilities = list([s, t])
        possibilities = list([input_array0, input_array1])
        #### reduce = lambda possibility: If(equal(* possibility), ["Equal", "Not equal"])
        reduce = (lambda possibility: if_(eq(* possibility), ['Equal', 'Not equal']))
        #### return reduce(map(mapping0, possibilities))
        return reduce(map(mapping0, possibilities))
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