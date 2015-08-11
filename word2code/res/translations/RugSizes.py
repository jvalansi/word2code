from problem_utils import *


class RugSizes:
    def rugCount(self, area):
        input_int = area
        ways = list(combinations_with_replacement(range(inclusive(area)), 2))
        
        # Rugs come in various sizes.
        # In fact, we can find a rug with any integer width and length, except that no rugs have a distinct width and length that are both even integers.
        def valid(rug):
            #### reduce = lambda possibility: no((distinct(*rug) and both(possibility)))
            reduce = (lambda possibility: not_((ne(*rug) and all(possibility))))
            #### mapping = lambda integer: even(integer)
            mapping = (lambda integer: is_even(integer))
            #### possibilities = rug
            possibilities = rug
            #### return(reduce(map(mapping, possibilities)))
            return reduce(map(mapping, possibilities))
        # For example, we can find a 4x4 rug, but not a 2x4 rug.
        # We want to know how many different choices we have for a given area.
        # Create a class RugSizes the contains a method rugCount that is given the desired area and returns the number of different ways in which we can choose a rug size that will cover that exact area.
        # 
        # Do not count the same size twice -- a 6 x 9 rug and a 9 x 6 rug should be counted as one choice.

def example0():
	cls = RugSizes()
	input0 = 4
	returns = 2
	result = cls.rugCount(input0)
	return result == returns


def example1():
	cls = RugSizes()
	input0 = 8
	returns = 1
	result = cls.rugCount(input0)
	return result == returns



if __name__ == '__main__':
	print(example0()&example1())