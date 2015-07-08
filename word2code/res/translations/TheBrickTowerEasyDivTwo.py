from utils import *
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
        # The number of red bricks they have is redCount and each of them has a height of redHeight .
        # The number of blue bricks they have is blueCount and each of them has a height of blueHeight .
        # A tower is built by placing bricks one atop another.
        towers = transformations(red+blue)
        # A brick can be placed either on the ground, or on a brick of a different color.
        # (I.e., you are not allowed to put two bricks of the same color immediately on one another.)
        immediately = csubsets
        two = 2
        same = eq
        no = not_
        def valid(tower): return tower and no(list(same(*bricks) for bricks in immediately(tower, two)))
        # A tower has to consist of at least one brick.
        # The height of a tower is the sum of all heights of bricks that form the tower.
        # ROOT-0(root=sum-8(nsubj=height-2(det=The-1, prep_of=tower-5(det=a-4)), cop=is-6, det=the-7, prep_of=heights-11(det=all-10, prep_of=bricks-13(rcmod=form-15(nsubj=that-14, dobj=tower-17(det=the-16))))))
        def height(tower): return sum(tower)
        # Two towers are considered to be different if they have different heights.
        # (Two towers of the same height are considered the same, even if they differ in the number and colors of bricks that form them.)
        # You are given the ints redCount , redHeight , blueCount and blueHeight .
        # Return the number of different towers that John and Brus can build.
        number = len
        different = set
        return(number(different(map(height, (filter(valid, towers))))))



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
	print(example0()&example1()&example2())