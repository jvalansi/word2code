from problem_utils import *

class BlockTower:
	def getTallest(self, blockHeights):
		input_array = blockHeights
		N = len(input_array)
		possibilities = transformations(input_array)
		# Josh loves playing with blocks. 
		# Currently, he has N blocks, labeled 0 through N-1. 
		# The heights of all blocks are positive integers. 
		# More precisely, for each i, the height of block i is blockHeights[i].
		# Josh is interested in making the tallest block tower possible. 
		# He likes all his towers to follow three simple rules:
		
		# The blocks must be stacked in a single column, one atop another. 
		# The labels of blocks used in the tower must increase from the bottom to the top. 
		# In other words, whenever Josh places box x on top of box y, we have x > y.
		# Josh will never place a box of an even height on top of a box of an odd height.
		valid = lambda possibility: (all([pair[0] > pair[1] for pair in cpairs(possibility)]) 
							and not any([is_even(pair[0]) and is_odd(pair[1]) for pair in cpairs(possibility)]))
		
				# The labels of blocks used in the tower must increase from the bottom to the top. 
		# In other words, whenever Josh places box x on top of box y, we have x > y.
		#### valid = lambda possibility: whenever(x > y for x, y in pairs(possibility) if top(x, y)) 
		valid = lambda possibility: all(pair0 > pair1 for pair0, pair1 in pairs(possibility) if successive(pair0, pair1)) 

		# Josh will never place a box of an even height on top of a box of an odd height.
		#### valid = lambda possibility: never([even(box) and odd(box) for box, box in pairs(possibility) if top(box, box)])
		valid = lambda possibility: not_any([is_even(pair0) and is_odd(pair1) for pair0, pair1 in pairs(possibility) if successive(pair0, pair1)])
		
		# The height of the tower is simply the sum of heights of all its blocks.
		#### height = lambda tower: sum(heights)
		mapping = lambda possibility: sum(possibility)
		
		# You are given the int[] blockHeights. 
		# Return the height of the tallest possible block tower Josh can build.
		#### return(tallest([height(possibility) for possibility in tower if can(possibility)]))
		return(max([mapping(possibility) for possibility in possibilities if valid(possibility)]))
	
if __name__ == '__main__':
	blockHeights = [4,7]
	bt = BlockTower()
	print(bt.getTallest(blockHeights))