from utils import *

class TopFox:
    def possibleHandles(self, familyName, givenName):
        input_array0 = familyName
        input_array1 = givenName
        # Fox Ciel is planning to register on TopFox.
        # Her family name is familyName and her given name is givenName .
        # She will choose a TopFox handle according to the following rule.
        # Let s be a non-empty prefix of her family name and let t be a non-empty prefix of her given name.
        s = prefix(familyName)
        t = prefix(givenName)
        # Now Fox Ciel may choose the concatenation of s and t as her handle.
        def possible(handle) : concatentaion(s,t)
        # For example, suppose Fox Ciel's family name is "fox" and her given name is "ciel".
        # She may choose the handle "foxciel", "fc", or "foxc".
        # She may not choose "ox", "ciel", or "jiro".
        # You are told Fox Ciel's family name and given name.
        # Return the number of possible handles Fox Ciel may choose.
        return(number(possible(handles)))



def example0():
	cls = TopFox()
	input0 = "ab"
	input1 = "cd"
	returns = 4
	result = cls.possibleHandles(input0, input1)
	return result == returns


def example1():
	cls = TopFox()
	input0 = "abb"
	input1 = "bbc"
	returns = 7
	result = cls.possibleHandles(input0, input1)
	return result == returns


def example2():
	cls = TopFox()
	input0 = "fox"
	input1 = "ciel"
	returns = 12
	result = cls.possibleHandles(input0, input1)
	return result == returns


def example3():
	cls = TopFox()
	input0 = "abbbb"
	input1 = "bbbbbbbc"
	returns = 16
	result = cls.possibleHandles(input0, input1)
	return result == returns


def example4():
	cls = TopFox()
	input0 = "abxy"
	input1 = "xyxyxc"
	returns = 21
	result = cls.possibleHandles(input0, input1)
	return result == returns


def example5():
	cls = TopFox()
	input0 = "ababababab"
	input1 = "bababababa"
	returns = 68
	result = cls.possibleHandles(input0, input1)
	return result == returns



if __name__ == '__main__':
	print(example0())