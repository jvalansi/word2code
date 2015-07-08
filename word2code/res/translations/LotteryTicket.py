from utils import *

class LotteryTicket:
	def buy(self, price, b1, b2, b3, b4):
		input_int0 = price
		input_int1 = b1
		input_int2 = b2
		input_int3 = b3
		input_int4 = b4
		#  Nick likes to play the lottery.
		# The cost of a single lottery ticket is price .
		# Nick has exactly four banknotes with values b1 , b2 , b3 and b4 (some of the values may be equal).
		# He wants to know if it's possible to buy a single lottery ticket without getting any change back.
		# In other words, he wants to pay the exact price of a ticket using any subset of his banknotes.
		# Return "POSSIBLE" if it is possible or "IMPOSSIBLE" if it is not (all quotes for clarity). 
		pass

def example0():
	cls = LotteryTicket()
	input0 = 10
	input1 = 1
	input2 = 5
	input3 = 10
	input4 = 50
	returns = "POSSIBLE"
	result = cls.buy(input0, input1, input2, input3, input4)
	return result == returns

def example1():
	cls = LotteryTicket()
	input0 = 15
	input1 = 1
	input2 = 5
	input3 = 10
	input4 = 50
	returns = "POSSIBLE"
	result = cls.buy(input0, input1, input2, input3, input4)
	return result == returns

def example2():
	cls = LotteryTicket()
	input0 = 65
	input1 = 1
	input2 = 5
	input3 = 10
	input4 = 50
	returns = "POSSIBLE"
	result = cls.buy(input0, input1, input2, input3, input4)
	return result == returns

def example3():
	cls = LotteryTicket()
	input0 = 66
	input1 = 1
	input2 = 5
	input3 = 10
	input4 = 50
	returns = "POSSIBLE"
	result = cls.buy(input0, input1, input2, input3, input4)
	return result == returns

def example4():
	cls = LotteryTicket()
	input0 = 1000
	input1 = 999
	input2 = 998
	input3 = 997
	input4 = 996
	returns = "IMPOSSIBLE"
	result = cls.buy(input0, input1, input2, input3, input4)
	return result == returns

def example5():
	cls = LotteryTicket()
	input0 = 20
	input1 = 5
	input2 = 5
	input3 = 5
	input4 = 5
	returns = "POSSIBLE"
	result = cls.buy(input0, input1, input2, input3, input4)
	return result == returns

def example6():
	cls = LotteryTicket()
	input0 = 2
	input1 = 1
	input2 = 5
	input3 = 10
	input4 = 50
	returns = "IMPOSSIBLE"
	result = cls.buy(input0, input1, input2, input3, input4)
	return result == returns

if __name__ == '__main__':
	print(example0())

