from utils import *

class FingerCounting:
	def maxNumber(self, weakFinger, maxCount):
		input_int0 = weakFinger
		input_int1 = maxCount
		#  Your little son is counting numbers with his left hand.
		# Starting with his thumb and going toward his pinky, he counts each finger in order.
		# After counting his pinky, he reverses direction and goes back toward his thumb.
		# He repeats this process until he reaches his target number.
		# He never skips a finger.
		# For example, to count to ten, he would count: thumb, index, middle, ring, pinky, ring, middle, index, thumb, index.
		# Sadly, one of his fingers hurts and he can only count on it a limited number of times.
		# His fingers are numbered 1 through 5 from thumb to pinky.
		# You are given an int weakFinger , the finger that hurts, and an int maxCount , the maximum number of times he can use that finger.
		# Return the largest number he can count to.
		# If he cannot even begin counting, return 0. 
		pass

def example0():
	cls = FingerCounting()
	input0 = 2
	input1 = 3
	returns = 15
	result = cls.maxNumber(input0, input1)
	return result == returns

def example1():
	cls = FingerCounting()
	input0 = 1
	input1 = 0
	returns = 0
	result = cls.maxNumber(input0, input1)
	return result == returns

def example2():
	cls = FingerCounting()
	input0 = 5
	input1 = 0
	returns = 4
	result = cls.maxNumber(input0, input1)
	return result == returns

def example3():
	cls = FingerCounting()
	input0 = 2
	input1 = 48
	returns = 193
	result = cls.maxNumber(input0, input1)
	return result == returns

def example4():
	cls = FingerCounting()
	input0 = 5
	input1 = 973
	returns = 7788
	result = cls.maxNumber(input0, input1)
	return result == returns

def example5():
	cls = FingerCounting()
	input0 = 3
	input1 = 99999
	returns = 399998
	result = cls.maxNumber(input0, input1)
	return result == returns

if __name__ == '__main__':
	print(example0())

