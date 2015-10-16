from problem_utils import *
from operator import *


class IdentifyingWood:
    def check(self, s, t):
        input_array0 = s
        input_array1 = t
        
        
        
        
        # We call a pair of Strings (input_array0, input_array1) "wood" if input_array1 is contained in input_array0 as a subsequence.
        def reduce0(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = lambda possibility: contained(* possibility)
            reduce = (lambda possibility: contains(* possibility))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # (See Notes for a formal definition.)
        # Given Strings input_array0 and input_array1, return the String "Yep, it'input_array0 wood." (quotes for clarity) if the pair (input_array0, input_array1) is wood and "Nope." otherwise.
        #### possibilities = list([s, t])
        possibilities = list([input_array0, input_array1])
        #### reduce = lambda possibility: if(possibility, ["Yep, it's wood.", "Nope."]))
        reduce = (lambda possibility: if_(possibility, ["Yep, it's wood.", "Nope."]))
        #### return reduce(wood(possibilities))
        return reduce(reduce0(possibilities))

def example0():
	cls = IdentifyingWood()
	input0 = "absdefgh"
	input1 = "asdf"
	returns = "Yep, it's wood."
	result = cls.check(input0, input1)
	return result == returns

def example1():
	cls = IdentifyingWood()
	input0 = "oxoxoxox"
	input1 = "ooxxoo"
	returns = "Nope."
	result = cls.check(input0, input1)
	return result == returns

def example2():
	cls = IdentifyingWood()
	input0 = "oxoxoxox"
	input1 = "xxx"
	returns = "Yep, it's wood."
	result = cls.check(input0, input1)
	return result == returns

def example3():
	cls = IdentifyingWood()
	input0 = "qwerty"
	input1 = "qwerty"
	returns = "Yep, it's wood."
	result = cls.check(input0, input1)
	return result == returns

def example4():
	cls = IdentifyingWood()
	input0 = "string"
	input1 = "longstring"
	returns = "Nope."
	result = cls.check(input0, input1)
	return result == returns

if __name__ == '__main__':
    print(example0())