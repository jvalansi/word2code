from problem_utils import *


class UniqueDigits:
    def count(self, n):
        input_int = n
        inf = 10000
        
        # Given an int n find all positive integers less than n whose digits are all different.
        def valid(possibility):
            #### reduce = lambda possibility: (positive(integer) and less_than(integer, n) and all(possibility))
            reduce = (lambda possibility0: (is_positive(possibility) and lt(possibility, n) and all(possibility0)))
            #### mapping = lambda digits: different(*digits)
            mapping = (lambda digits: ne(*digits))
            #### possibilities = pairs(str(integer))
            possibilities = pairs(str(possibility))
            #### return(reduce(map(mapping, possibilities)))
            return reduce(map(mapping, possibilities))
        # Return the total number of such integers.
        #### return number(filter(such, integers(inf)))
        return len(filter(valid, range(inf)))

def example0():
	cls = UniqueDigits()
	input0 = 21
	returns = 19
	result = cls.count(input0)
	return result == returns


def example1():
	cls = UniqueDigits()
	input0 = 101
	returns = 90
	result = cls.count(input0)
	return result == returns


def example2():
	cls = UniqueDigits()
	input0 = 1001
	returns = 738
	result = cls.count(input0)
	return result == returns


def example3():
	cls = UniqueDigits()
	input0 = 1
	returns = 0
	result = cls.count(input0)
	return result == returns



if __name__ == '__main__':
	print(example0()&example1()&example2()&example3())