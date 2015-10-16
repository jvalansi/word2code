from problem_utils import *


class BlockTower:
    def getTallest(self, blockHeights):
        input_array = blockHeights
        N = len(input_array)
        
        
        
        
        # Josh loves playing with blocks.
        # Currently, he has N blocks, labeled 0 through N-1.
        # The heights of all blocks are positive integers.
        # More precisely, for each i, the height of block i is input_array[i].
        # Josh is interested in making the tallest block tower possible.
        # He likes all his towers to follow three simple rules:
        # The labels of blocks used in the tower must increase from the bottom to the top.
        # In other words, whenever Josh places box x on top of box y, we have x > y.
        def valid0(possibility):
            #### possibilities = top(possibility)
            possibilities = cpairs(possibility)
            #### def mapping(box): return >(* box)
            def mapping(possibility): return gt(* possibility)
            #### def reduce(box): return whenever(box)
            def reduce(possibility): return all(possibility)
            #### return reduce(map(mapping, possibilities))
            return reduce(map(mapping, possibilities))
        # Josh will never place a box of an even height on top of a box of an odd height.
        def valid1(possibility):
            #### possibilities = top(possibility)
            possibilities = cpairs(possibility)
            #### def mapping(possibility): return even(box[0])
            def mapping(possibility): return is_even(possibility[0])
            #### def valid(possibility): return odd(box[1])
            def valid(possibility): return is_odd(possibility[1])
            #### def reduce(possibility): return never(possibility)
            def reduce(possibility): return not_(possibility)
            #### return reduce(map(mapping, filter(valid, possibilities)))
            return reduce(map(mapping, filter(valid, possibilities)))
        # The height of the tower is simply the sum of heights of all its blocks.
        def mapping0(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = lambda possibility: sum(heights)
            reduce = lambda possibility: sum(possibility)
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # You are given the int[] input_array.
        # Return the height of the tallest possible block tower Josh can build.
        #### possibilities = transformations(input_array)
        possibilities = transformations(input_array)
        #### def reduce(possibility): return tallest(tower)
        def reduce(possibility): return max(possibility)
        #### return reduce(map(mapping0, filter(valid1, filter(valid0, possibilities))))
        return reduce(map(mapping0, filter(valid1, filter(valid0, possibilities))))

def example0():
	cls = BlockTower()
	input0 = [4,7]
	returns = 11
	result = cls.getTallest(input0)
	return result == returns

def example1():
	cls = BlockTower()
	input0 = [7,4]
	returns = 7
	result = cls.getTallest(input0)
	return result == returns

def example2():
	cls = BlockTower()
	input0 = [7]
	returns = 7
	result = cls.getTallest(input0)
	return result == returns

def example3():
	cls = BlockTower()
	input0 = [4]
	returns = 4
	result = cls.getTallest(input0)
	return result == returns

def example4():
	cls = BlockTower()
	input0 = [48,1,50,1,50,1,48]
	returns = 196
	result = cls.getTallest(input0)
	return result == returns

def example5():
	cls = BlockTower()
	input0 = [49,2,49,2,49]
	returns = 147
	result = cls.getTallest(input0)
	return result == returns

def example6():
	cls = BlockTower()
	input0 = [44,3,44,3,44,47,2,47,2,47,2]
	returns = 273
	result = cls.getTallest(input0)
	return result == returns

if __name__ == '__main__':
    print(example0())