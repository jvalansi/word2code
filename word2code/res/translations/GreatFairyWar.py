from problem_utils import *

class GreatFairyWar:
	def minHP(self, dps, hp):
		input_array0 = dps
		input_array1 = hp
		#  You are a wizard.
		# You are facing N fairies, numbered 0 through N-1.
		# Your goal is to defeat all of them.
		# You can only attack one fairy at a time.
		# Moreover, you must fight the fairies in order: you can only attack fairy X+1 after you defeat fairy X.
		# On the other hand, all fairies that have not been defeated yet will attack you all the time.
		# Each fairy has two characteristics: her damage per second (dps) and her amount of hit points.
		# Your damage per second is 1.
		# That is, you are able to reduce an opponent's hit points by 1 each second.
		# In other words, if a fairy has H hit points, it takes you H seconds to defeat her.
		# You are given two int[]s, each of length N: dps and hp .
		# For each i, dps [i] is the damage per second of fairy i, and hp [i] is her initial amount of hit points.
		# We assume that your number of hit points is sufficiently large to avoid defeat when fighting the fairies.
		# Compute and return the total number of hit points you'll lose during the fight.
		# In other words, return the total amount of damage the attacking fairies will deal. 
		pass

def example0():
	cls = GreatFairyWar()
	input0 = [1,2]
	input1 = [3,4]
	returns = 17
	result = cls.minHP(input0, input1)
	return result == returns

def example1():
	cls = GreatFairyWar()
	input0 = [1,1,1,1,1,1,1,1,1,1]
	input1 = [1,1,1,1,1,1,1,1,1,1]
	returns = 55
	result = cls.minHP(input0, input1)
	return result == returns

def example2():
	cls = GreatFairyWar()
	input0 = [20,12,10,10,23,10]
	input1 = [5,7,7,5,7,7]
	returns = 1767
	result = cls.minHP(input0, input1)
	return result == returns

def example3():
	cls = GreatFairyWar()
	input0 = [5,7,7,5,7,7]
	input1 = [20,12,10,10,23,10]
	returns = 1998
	result = cls.minHP(input0, input1)
	return result == returns

def example4():
	cls = GreatFairyWar()
	input0 = [30,2,7,4,7,8,21,14,19,12]
	input1 = [2,27,18,19,14,8,25,13,21,30]
	returns = 11029
	result = cls.minHP(input0, input1)
	return result == returns

def example5():
	cls = GreatFairyWar()
	input0 = [1]
	input1 = [1]
	returns = 1
	result = cls.minHP(input0, input1)
	return result == returns

if __name__ == '__main__':
	print(example0())

