from utils import *

class EllysSubstringSorter:
	def getMin(self, S, L):
		input_array = S
		input_int = L
		#  Elly has a String S of uppercase letters and a magic device that can modify the string.
		# The strength of the device is an int L .
		# The device does the following: The user enters a 0-based index i such that 0 <= i <= length( S )- L .
		# The device then takes L letters of S , starting at index i, and puts these letters into alphabetical order.
		# Formally, the letters that get reordered are the letters S [i], S [i+1], and so on, until and including S [i+ L -1].
		# For example, let S ="TOPCODER" and let L =4.
		# If the user chooses i=0, the selected substring will be "TOPC".
		# These letters are rearranged into alphabetical order ("COPT") while the rest of the string remains unchanged ("....ODER").
		# Thus, the result would be the string "COPTODER".
		# If the user were to choose i=2 instead, the resulting string would be "TOCDOPER".
		# Here, "TO....ER" was left unchanged, and "PCOD" was changed into "CDOP".
		# Elly's magic device has a flaw: it can only be used once and then it self-destructs.
		# You are given the String S and the int L described above.
		# Return the lexicographically smallest string Elly can create by using the device exactly once. 
		pass

def example0():
	cls = EllysSubstringSorter()
	input0 = "TOPCODER"
	input1 = 4
	returns = "COPTODER"
	result = cls.getMin(input0, input1)
	return result == returns

def example1():
	cls = EllysSubstringSorter()
	input0 = "ESPRIT"
	input1 = 3
	returns = "EPRSIT"
	result = cls.getMin(input0, input1)
	return result == returns

def example2():
	cls = EllysSubstringSorter()
	input0 = "AAAAAAAAA"
	input1 = 2
	returns = "AAAAAAAAA"
	result = cls.getMin(input0, input1)
	return result == returns

def example3():
	cls = EllysSubstringSorter()
	input0 = "ABRACADABRA"
	input1 = 5
	returns = "AAABCRDABRA"
	result = cls.getMin(input0, input1)
	return result == returns

def example4():
	cls = EllysSubstringSorter()
	input0 = "BAZINGA"
	input1 = 6
	returns = "ABGINZA"
	result = cls.getMin(input0, input1)
	return result == returns

def example5():
	cls = EllysSubstringSorter()
	input0 = "AAAWDIUAOIWDESBEAIWODJAWDBPOAWDUISAWDOOPAWD"
	input1 = 21
	returns = "AAAAAABDDDEEIIIJOOSUWWWWDBPOAWDUISAWDOOPAWD"
	result = cls.getMin(input0, input1)
	return result == returns

if __name__ == '__main__':
	print(example0())

