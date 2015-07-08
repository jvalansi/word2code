from utils import *

class CucumberMarket:
	def check(self, price, budget, k):
		input_array = price
		input_int0 = budget
		input_int1 = k
		#  Cucumber Boy is young and loves cucumbers.
		# Therefore, Cucumber Boy will go to the cucumber market to buy some cucumbers.
		# Different cucumbers may have different costs.
		# For each i, buying the i-th cucumber (0-based index) costs price [i] yen.
		# Cucumber Boy's mother gave him budget yen.
		# However, he does not understand money well.
		# He just chooses some k unique cucumbers he likes.
		# If the total price of the chosen cucumbers is not greater than budget yen, he can buy them, otherwise he cannot.
		# You are given the int[] price , the int budget and the int k .
		# Your method must return "YES" (quotes for clarity) if Cucumber Boy can buy any set of k unique cucumbers, and "NO" if there is some set of k cucumbers that is too expensive for him. 
		pass

def example0():
	cls = CucumberMarket()
	input0 = [1000,1,10,100]
	input1 = 1110
	input2 = 3
	returns = "YES"
	result = cls.check(input0, input1, input2)
	return result == returns

def example1():
	cls = CucumberMarket()
	input0 = [1000,1,10,100]
	input1 = 1109
	input2 = 3
	returns = "NO"
	result = cls.check(input0, input1, input2)
	return result == returns

def example2():
	cls = CucumberMarket()
	input0 = [33,4]
	input1 = 33
	input2 = 1
	returns = "YES"
	result = cls.check(input0, input1, input2)
	return result == returns

def example3():
	cls = CucumberMarket()
	input0 = [1,1,1,1,1,1]
	input1 = 2
	input2 = 4
	returns = "NO"
	result = cls.check(input0, input1, input2)
	return result == returns

def example4():
	cls = CucumberMarket()
	input0 = [1000,1000,1000,1000,1000,1000,1000,1000,1000]
	input1 = 10000
	input2 = 9
	returns = "YES"
	result = cls.check(input0, input1, input2)
	return result == returns

if __name__ == '__main__':
	print(example0())

