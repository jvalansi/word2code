from problem_utils import *

class MnemonicMemory:
	def getPhrase(self, number, dictionary):
		input_array0 = number
		input_array1 = dictionary
		#  It is often helpful to have a mnemonic phrase handy for a math test.
		# For example, the number 25735 can be remembered as "is there anybody out there".
		# If we count the number of characters in every word, we would get the sequence 2, 5, 7, 3, 5, which represents the original number!
		# Unfortunately for you, your professor likes to make the students memorize random numbers and then test them.
		# To beat the system, your plan is to come up with mnemonic phrases that will represent the numbers you must memorize.
		# You are given a String number and a String[] dictionary .
		# Return a single space delimited list of words, where each word is an element of dictionary , and no element of dictionary is used more than once.
		# The phrase must contain exactly n words, where n is the number of digits in the number , and the length of the i-th word must be equal to the i-th digit of the number for all i.
		# If more than one phrase is possible, return the one that comes first alphabetically (in other words, if you have several words of the same length, you should use them in alphabetical order). 
		pass

def example0():
	cls = MnemonicMemory()
	input0 = "25735"
	input1 = ["is", "there", "anybody", "out", "there"]
	returns = "is there anybody out there"
	result = cls.getPhrase(input0, input1)
	return result == returns

def example1():
	cls = MnemonicMemory()
	input0 = "31415926"
	input1 = ["may", "i", "have", "a", "large", "container", "of", "coffee"]
	returns = "may a have i large container of coffee"
	result = cls.getPhrase(input0, input1)
	return result == returns

def example2():
	cls = MnemonicMemory()
	input0 = "1212"
	input1 = ["a", "aa", "a", "aa"]
	returns = "a aa a aa"
	result = cls.getPhrase(input0, input1)
	return result == returns

def example3():
	cls = MnemonicMemory()
	input0 = "11111111122"
	input1 = ["a", "b", "d", "c", "a", "e", "f", "z", "zz", "za", "az", "e"]
	returns = "a a b c d e e f z az za"
	result = cls.getPhrase(input0, input1)
	return result == returns

def example4():
	cls = MnemonicMemory()
	input0 = "2222"
	input1 = ["ab", "cd", "ef", "a", "b", "ab"]
	returns = "ab ab cd ef"
	result = cls.getPhrase(input0, input1)
	return result == returns

if __name__ == '__main__':
	print(example0())

