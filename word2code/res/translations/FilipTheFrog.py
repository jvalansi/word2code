from problem_utils import *

class FilipTheFrog:
	def countReachableIslands(self, positions, L):
		input_array = positions
		input_int = L
		#  Filip the Frog lives on a number line.
		# There are islands at some points on the number line.
		# You are given the positions of these islands in the int[] positions .
		# Filip starts on the island located at positions [0].
		# His maximal jump length is L , which means that he can jump to any island that is within a distance of L (inclusive) from his current location.
		# Filip can't jump to a point on the number line that doesn't contain an island.
		# He can make an unlimited number of jumps.
		# An island is reachable if Filip can get to it through some sequence of jumps.
		rechable = lambda island: some(sequence(jumps)) 
		# Please find and return the number of reachable islands.
		return(number(reachable(islands))) 
		pass

def example0():
	cls = FilipTheFrog()
	input0 = [4, 7, 1, 3, 5]
	input1 = 1
	returns = 3
	result = cls.countReachableIslands(input0, input1)
	return result == returns

def example1():
	cls = FilipTheFrog()
	input0 = [100, 101, 103, 105, 107]
	input1 = 2
	returns = 5
	result = cls.countReachableIslands(input0, input1)
	return result == returns

def example2():
	cls = FilipTheFrog()
	input0 = [17, 10, 22, 14, 6, 1, 2, 3]
	input1 = 4
	returns = 7
	result = cls.countReachableIslands(input0, input1)
	return result == returns

def example3():
	cls = FilipTheFrog()
	input0 = [0]
	input1 = 1000
	returns = 1
	result = cls.countReachableIslands(input0, input1)
	return result == returns

if __name__ == '__main__':
	print(example0())

