from problem_utils import *

class ElectronicPetEasy:
	def isDifficult(self, st1, p1, t1, st2, p2, t2):
		input_int0 = st1
		input_int1 = p1
		input_int2 = t1
		input_int3 = st2
		input_int4 = p2
		input_int5 = t2
		#  Kirino has found a game in which she has to feed electronic pets.
		# There are two pets in the game.
		# You are given six ints st1 , p1 , t1 , st2 , p2 , t2 .
		# To win the game, Kirino must satisfy the following rules: She must feed her first pet for the first time precisely at the time st1 .
		# There must be exactly p1 seconds between any two consecutive feedings of the first pet.
		# She must feed the first pet exactly t1 times.
		# She must feed her second pet for the first time precisely at the time st2 .
		# There must be exactly p2 seconds between any two consecutive feedings of the second pet.
		# She must feed the second pet exactly t2 times.
		# Feeding the pets is easy if Kirino never needs to feed both pets at the same time.
		# Return "Easy" (quotes for clarity) if feeding the pets is easy for the given inputs.
		# Otherwise, return "Difficult".
		# Note that the return value is case-sensitive. 
		pass

def example0():
	cls = ElectronicPetEasy()
	input0 = 3
	input1 = 3
	input2 = 3
	input3 = 5
	input4 = 2
	input5 = 3
	returns = "Difficult"
	result = cls.isDifficult(input0, input1, input2, input3, input4, input5)
	return result == returns

def example1():
	cls = ElectronicPetEasy()
	input0 = 3
	input1 = 3
	input2 = 3
	input3 = 5
	input4 = 2
	input5 = 2
	returns = "Easy"
	result = cls.isDifficult(input0, input1, input2, input3, input4, input5)
	return result == returns

def example2():
	cls = ElectronicPetEasy()
	input0 = 1
	input1 = 4
	input2 = 7
	input3 = 1
	input4 = 4
	input5 = 7
	returns = "Difficult"
	result = cls.isDifficult(input0, input1, input2, input3, input4, input5)
	return result == returns

def example3():
	cls = ElectronicPetEasy()
	input0 = 1
	input1 = 1000
	input2 = 1000
	input3 = 2
	input4 = 1000
	input5 = 1000
	returns = "Easy"
	result = cls.isDifficult(input0, input1, input2, input3, input4, input5)
	return result == returns

def example4():
	cls = ElectronicPetEasy()
	input0 = 1
	input1 = 1
	input2 = 1
	input3 = 2
	input4 = 2
	input5 = 2
	returns = "Easy"
	result = cls.isDifficult(input0, input1, input2, input3, input4, input5)
	return result == returns

if __name__ == '__main__':
	print(example0())

