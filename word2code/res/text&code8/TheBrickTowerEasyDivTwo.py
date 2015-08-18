from problem_utils import *
from itertools import combinations


class TheBrickTowerEasyDivTwo:
    def find(self, redCount, redHeight, blueCount, blueHeight):
        input_int0 = redCount
        input_int1 = redHeight
        input_int2 = blueCount
        input_int3 = blueHeight
        red = [redHeight]*redCount
        blue = [blueHeight]*blueCount
        
        
        # John and Brus are building towers using toy bricks.
        # They have two types of bricks: red and blue ones.
        # The number of red bricks they have is input_int0 and each of them has a height of input_int1 .
        # The number of blue bricks they have is input_int2 and each of them has a height of input_int3 .
        # A tower is built by placing bricks one atop another.
        # A brick can be placed either on the ground, or on a brick of a different color.
        # (I.e., you are not allowed to put two bricks of the same color immediately on one another.)
        def valid0(possibility):
            #### def reduce(possibility): return (tower and no(list(possibility)))
            def reduce(possibility0): return (possibility and not_(list(possibility0)))
            #### def mapping(bricks): return bricks
            def mapping(bricks): return bricks
            #### possibilities = two(tower)
            possibilities = cpairs(possibility)
            #### def valid(bricks): return same(*bricks)
            def valid(bricks): return eq(*bricks)
            #### return(reduce(map(mapping, filter(valid, possibilities))))
            return reduce(map(mapping, filter(valid, possibilities)))
        # A tower has to consist of at least one brick.
        # The height of a tower is the sum of all heights of bricks that form the tower.
        def mapping0(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = lambda possibility: sum(tower)
            reduce = (lambda possibility: sum(possibility))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # Two towers are considered to be different if they have different heights.
        # (Two towers of the same height are considered the same, even if they differ in the number and colors of bricks that form them.)
        # You are given the ints input_int0 , input_int1 , input_int2 and input_int3 .
        # Return the number of different towers that John and Brus can build.
        #### towers = transformations(red+blue)
        possibilities = transformations((red + blue))
        #### def reduce(possibility): return number(different(possibility))
        def reduce(possibility): return len(set(possibility))
        #### return reduce(map(height, filter(valid0, towers))))
        return reduce(map(mapping0, filter(valid0, possibilities)))

def example0():
	cls = TheBrickTowerEasyDivTwo()
	input0 = 1
	input1 = 2
	input2 = 3
	input3 = 4
	returns = 4
	result = cls.find(input0, input1, input2, input3)
	return result == returns


def example1():
	cls = TheBrickTowerEasyDivTwo()
	input0 = 4
	input1 = 4
	input2 = 4
	input3 = 7
	returns = 12
	result = cls.find(input0, input1, input2, input3)
	return result == returns


def example2():
	cls = TheBrickTowerEasyDivTwo()
	input0 = 7
	input1 = 7
	input2 = 4
	input3 = 4
	returns = 13
	result = cls.find(input0, input1, input2, input3)
	return result == returns


def example3():
	cls = TheBrickTowerEasyDivTwo()
	input0 = 47
	input1 = 47
	input2 = 47
	input3 = 47
	returns = 94
	result = cls.find(input0, input1, input2, input3)
	return result == returns



if __name__ == '__main__':
	print(example0())