from problem_utils import *
from string import lowercase


class ValueOfString:
    def findValue(self, s):
        s = list(s)
        input_array = s
        N = len(s)
        
        # You are given a String s consisting of lower case letters.
        # We assign the letters 'a' to 'z' values of 1 to 26, respectively.
        # We will denote the value assigned to the letter X by val[X].
        #### val = dict(zip(list(lowercase),range(1,inclusive(26))))
        possibilities = dict(zip(list(lowercase), range(1, inclusive(26))))
        # For example, val['a'] = 1 and val['e'] = 5.
        # We define the value of the string s as follows.
        # For each letter s[i], let k[i] be the number of letters in s that are less than or equal to s[i], including s[i] itself.
        def mapping1(i):
            #### reduce = lambda possibility: number(possibility)
            reduce = (lambda possibility: sum(possibility))
            #### mapping = lambda letter: less_than_or_equal(letter, s[i])
            mapping = (lambda letter: le(letter, s[i]))
            #### possibilities = s
            possibilities = s
            #### return(reduce(map(mapping, possibilities)))
            return reduce(map(mapping, possibilities))
        # Then, the value of s is defined to be the sum of k[i] * val[s[i]] for all valid i.
        #### value = lambda s: sum(k(i)*val[s[i]] for i in range(N))
        mapping0 = lambda s: sum(((mapping1(i) * possibilities[s[i]]) for i in range(N)))
        # Given the string, compute and return the value of the string.
        #### return value(string)
        return mapping0(input_array)

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