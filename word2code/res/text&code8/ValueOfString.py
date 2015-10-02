from problem_utils import *
from string import lowercase


class ValueOfString:
    def findValue(self, s):
        s = list(s)
        input_array = s
        N = len(s)
        
        
        # You are given a String input_array consisting of lower case letters.
        # We assign the letters 'a' to 'z' values of 1 to 26, respectively.
        # We will denote the value assigned to the letter X by val[X].
        #### val = dict(zip(list(lowercase),range(1,inclusive(26))))
        possibilities = dict(zip(list(lowercase), range(1, inclusive(26))))
        # For example, val['a'] = 1 and val['e'] = 5.
        # We define the value of the string input_array as follows.
        # For each letter input_array[i], let k[i] be the number of letters in input_array that are less than or equal to input_array[i], including input_array[i] itself.
        def mapping1(possibility):
            #### def reduce(possibility): return number(possibility)
            def reduce(possibility): return sum(possibility)
            #### def mapping(letter): return less(letter, s[possibility])
            def mapping(letter): return le(letter, s[possibility])
            #### possibilities = s
            possibilities = s
            #### return(reduce(map(mapping, possibilities)))
            return reduce(map(mapping, possibilities))
        # Then, the value of input_array is defined to be the sum of k[i] * val[input_array[i]] for all valid i.
        def mapping0(possibility):
            #### reduce = lambda possibility: sum(possibility)
            reduce = (lambda possibility: sum(possibility))
            #### mapping = lambda i: (k(i) * val[s[i]])
            mapping = (lambda i: (mapping1(i) * possibilities[s[i]]))
            #### possibility = range(N)
            possibility = range(N)
            #### return(reduce(map(mapping, possibility)))
            return reduce(map(mapping, possibility))
        # Given the string, compute and return the value of the string.
        #### reduce = lambda possibility: value(string)
        reduce = (lambda possibility: mapping0(input_array))
        #### return(reduce(possibilities))
        return reduce(possibilities)

def example0():
	cls = ValueOfString()
	input0 = "babca"
	returns = 35
	result = cls.findValue(input0)
	return result == returns


def example1():
	cls = ValueOfString()
	input0 = "zz"
	returns = 104
	result = cls.findValue(input0)
	return result == returns


def example2():
	cls = ValueOfString()
	input0 = "y"
	returns = 25
	result = cls.findValue(input0)
	return result == returns


def example3():
	cls = ValueOfString()
	input0 = "aaabbc"
	returns = 47
	result = cls.findValue(input0)
	return result == returns


def example4():
	cls = ValueOfString()
	input0 = "topcoder"
	returns = 558
	result = cls.findValue(input0)
	return result == returns


def example5():
	cls = ValueOfString()
	input0 = "thequickbrownfoxjumpsoverthelazydog"
	returns = 11187
	result = cls.findValue(input0)
	return result == returns


def example6():
	cls = ValueOfString()
	input0 = "zyxwvutsrqponmlkjihgfedcba"
	returns = 6201
	result = cls.findValue(input0)
	return result == returns



if __name__ == '__main__':
	print(example0()&example1()&example2()&example3()&example4()&example5()&example6())