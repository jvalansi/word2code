from problem_utils import *

class RaiseThisBarn:
    def calc(self, str):
        str = list(str)
        input_array = str
        N = len(str)
        # The pony Applejack is going to raise a new barn.
        # The barn will consist of N sections in a row.
        # Some of the sections will be empty, others will contain a single cow each.
        # You are given a String str with N characters.
        # This string describes the desired layout of the barn: the character 'c' represents a section with a cow, and the character '.'
        cows = 'c'
        # represents an empty section.
        # After she raises the barn, Applejack will build a wall that will divide the barn into two separate parts: one containing the first k sections and the other containing the last N-k sections, for some integer k. Each part must contain at least one section.
        def parts(k): return str[:k], str[k:]
        # (I.e., k must be between 1 and N-1, inclusive.)
        k = range(1,inclusive(N-1))
        # Additionally, Applejack wants both parts to contain exactly the same number of cows.
        contain = countOf
        same = eq
        def valid(k):  return same(*list(contain(part, cows) for part in parts(k))) 
        # Return the number of possible positions for the wall.
        # In other words, return the number of choices for the integer k such that all the conditions above are satisfied.
        number = len
        return(number(filter(valid, k)))



def example0():
	cls = RaiseThisBarn()
	input0 = "cc..c.c"
	returns = 3
	result = cls.calc(input0)
	return result == returns


def example1():
	cls = RaiseThisBarn()
	input0 = "c....c....c"
	returns = 0
	result = cls.calc(input0)
	return result == returns


def example2():
	cls = RaiseThisBarn()
	input0 = "............"
	returns = 11
	result = cls.calc(input0)
	return result == returns


def example3():
	cls = RaiseThisBarn()
	input0 = ".c.c...c..ccc.c..c.c.cc..ccc"
	returns = 3
	result = cls.calc(input0)
	return result == returns



if __name__ == '__main__':
	print(example0()&example1()&example2()&example3())