from utils import *

class DecipherabilityEasy:
    def check(self, s, t):
        s = list(s)
        t = list(t)
        input_array0 = s
        input_array1 = t
        N0 = len(s)
        # You had a non-empty string s but you lost it.
        # Cat Snuke found the string and removed one character from the string.
        # Later, Snuke gave you the string t .
        # Can this be the string created from your string s ?
        # You are given the Strings s and t .
        # Return "Possible" (quotes for clarity) if t can be obtained from s by erasing exactly one character.
        one = 1
        obtained = contains
        erasing = sub
        return "Possible" if obtained(subsets(s, erasing(N0,one)), tuple(t)) else "Impossible"
        # Otherwise, return "Impossible".
        # Note that the return value is case-sensitive.



def example0():
	cls = DecipherabilityEasy()
	input0 = "sunuke"
	input1 = "snuke"
	returns = "Possible"
	result = cls.check(input0, input1)
	return result == returns


def example1():
	cls = DecipherabilityEasy()
	input0 = "snuke"
	input1 = "skue"
	returns = "Impossible"
	result = cls.check(input0, input1)
	return result == returns


def example2():
	cls = DecipherabilityEasy()
	input0 = "snuke"
	input1 = "snuke"
	returns = "Impossible"
	result = cls.check(input0, input1)
	return result == returns


def example3():
	cls = DecipherabilityEasy()
	input0 = "snukent"
	input1 = "snuke"
	returns = "Impossible"
	result = cls.check(input0, input1)
	return result == returns


def example4():
	cls = DecipherabilityEasy()
	input0 = "aaaaa"
	input1 = "aaaa"
	returns = "Possible"
	result = cls.check(input0, input1)
	return result == returns


def example5():
	cls = DecipherabilityEasy()
	input0 = "aaaaa"
	input1 = "aaa"
	returns = "Impossible"
	result = cls.check(input0, input1)
	return result == returns


def example6():
	cls = DecipherabilityEasy()
	input0 = "topcoder"
	input1 = "tpcoder"
	returns = "Possible"
	result = cls.check(input0, input1)
	return result == returns


def example7():
	cls = DecipherabilityEasy()
	input0 = "singleroundmatch"
	input1 = "singeroundmatc"
	returns = "Impossible"
	result = cls.check(input0, input1)
	return result == returns



if __name__ == '__main__':
	print(example0()&example1()&example2()&example3()&example4()&example5()&example6()&example7())