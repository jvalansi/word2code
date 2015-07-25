from problem_utils import *

class ContiguousCacheEasy:
	def bytesRead(self, n, k, addresses):
		input_array = addresses
		input_int0 = n
		input_int1 = k
		#  In order to make their newest microcontroller as cheap as possible, the ACME Widget Company designed it with a very simple cache.
		# The processor is connected to a slow memory system that contains n bytes, numbered 0 to n - 1.
		# The cache holds a copy of k of these bytes at a time, for fast access.
		# It has a base address (referred to as base below), and it holds a copy of the bytes numbered base , base +1, ..., base + k -1.
		# When a program reads a byte, the cache controller executes the following algorithm: Find a new range of k bytes which contains the requested byte, such that the difference between the old and new base addresses is minimized.
		# Note that if the requested byte was already in the cache, then the base address will not change.
		# Update the cache to the new range by reading from the memory system any bytes that are in the new range but not the old range, and discarding any bytes that were in the old range but not the new range.
		# Return the requested byte to the program.
		# To analyze the performance of a program, you wish to know how many bytes are read from the memory system.
		# The numbers of the bytes that the program reads are given in addresses , in the order that they are read.
		# When the program starts, the base address is 0. 
		pass

def example0():
	cls = ContiguousCacheEasy()
	input0 = 100
	input1 = 5
	input2 = [6, 0, 3, 20, 22, 16]
	returns = 13
	result = cls.bytesRead(input0, input1, input2)
	return result == returns

def example1():
	cls = ContiguousCacheEasy()
	input0 = 100
	input1 = 1
	input2 = [0, 4, 6, 6, 4, 10]
	returns = 4
	result = cls.bytesRead(input0, input1, input2)
	return result == returns

def example2():
	cls = ContiguousCacheEasy()
	input0 = 1000
	input1 = 999
	input2 = [0, 4, 123, 987, 999, 500, 0]
	returns = 2
	result = cls.bytesRead(input0, input1, input2)
	return result == returns

if __name__ == '__main__':
	print(example0())

