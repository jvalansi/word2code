from problem_utils import *


class RaiseThisBarn:
    def calc(self, str):
        str = list(str)
        input_array = str
        N = len(str)
        types = {'cows': 'c'}
        
        
        # The pony Applejack is going to raise a new barn.
        # The barn will consist of N sections in a row.
        # Some of the sections will be empty, others will contain a single cow each.
        # You are given a String input_array with N characters.
        # This string describes the desired layout of the barn: the character 'c' represents a section with a cow, and the character '.'
        # represents an empty section.
        # After she raises the barn, Applejack will build a wall that will divide the barn into two separate parts: one containing the first k sections and the other containing the last N-k sections, for some integer k. Each part must contain at least one section.
        def parts(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = lambda possibility: (str[:k], str[k:])
            reduce = (lambda possibility: (str[:possibility], str[possibility:]))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # (I.e., k must be between 1 and N-1, inclusive.)
        #### k = range(1,inclusive(N-1))
        possibilities = range(1, inclusive((N - 1)))
        # Additionally, Applejack wants both parts to contain exactly the same number of cows.
        def valid0(possibility):
            #### reduce = lambda possibility: same(*list(possibility))
            reduce = (lambda possibility: eq(*list(possibility)))
            #### mapping = lambda part: contain(part, cows)
            mapping = (lambda part: countOf(part, types['cows']))
            #### possibilities = parts(k)
            possibilities = parts(possibility)
            #### return(reduce(map(mapping, possibilities)))
            return reduce(map(mapping, possibilities))
        # Return the number of possible positions for the wall.
        # In other words, return the number of choices for the integer k such that all the conditions above are satisfied.
        #### return number(filter(valid0, k))
        return len(filter(valid0, possibilities))

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