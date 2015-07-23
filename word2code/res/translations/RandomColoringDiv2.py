from utils import *

class RandomColoringDiv2:
    def getCount(self, maxR, maxG, maxB, startR, startG, startB, d1, d2):
        input_int0 = maxR
        input_int1 = maxG
        input_int2 = maxB
        input_int3 = startR
        input_int4 = startG
        input_int5 = startB
        input_int6 = d1
        input_int7 = d2
        # Little Arthur has a new frisbee and he would like to color it.
        # A frisbee has the shape of a disc.
        # Arthur will color the disc using two colors: one for the top side, one for the bottom side.
        # Each color is defined by three integer components: R, G, and B (meaning red, green, and blue, respectively), where 0 <= R < maxR , 0 <= G < maxG , and 0 <= B < maxB .
        # It is known that Arthur can use any of the maxR * maxG * maxB possible colors.
        colors = product(range(maxR),range(maxG),range(maxB))
        # Arthur is going to perform the coloring in the following way: In the first step, he will color the top side of the frisbee using the color ( startR , startG , startB ).
        # In the second step, he will color the bottom side of the frisbee using a color that makes a good transition from the first color.
        # (This is explained below.)
        # A transition from color (R, G, B) to color (R', G', B') is called good if all components differ by at most d2 units (formally, |R - R'| <= d2 , |G - G'| <= d2 , |B - B'| <= d2 ) and at least one component differs by at least d1 units (formally, at least one of the conditions |R - R'| >= d1 , |G - G'| >= d1 , |B - B'| >= d1 holds).
        def good((R,G,B),(R_,G_, B_)): return all([abs(R - R_) <= d2 , abs(G - G_) <= d2 ,  abs(B - B_) <= d2]) and any([abs(R - R_) >= d1 , abs(G - G_) >= d1 , abs(B - B_) >= d1]) 
        # Intuitively, a transition between two colors is called good if they are neither too similar, nor too different.
        # After coloring the top side Arthur is wondering how many different options there are now for the color of the bottom side of the frisbee.
        # Given ints maxR , maxG , maxB , startR , startG , startB , d1 , and d2 , return the number of valid colors that make a good transition from the color ( startR , startG , startB ).
        number = len
        return(number([color for color in colors if good(( startR , startG , startB ),color)]))



def example0():
	cls = RandomColoringDiv2()
	input0 = 5
	input1 = 1
	input2 = 1
	input3 = 2
	input4 = 0
	input5 = 0
	input6 = 0
	input7 = 1
	returns = 3
	result = cls.getCount(input0, input1, input2, input3, input4, input5, input6, input7)
	return result == returns


def example1():
	cls = RandomColoringDiv2()
	input0 = 4
	input1 = 2
	input2 = 2
	input3 = 0
	input4 = 0
	input5 = 0
	input6 = 3
	input7 = 3
	returns = 4
	result = cls.getCount(input0, input1, input2, input3, input4, input5, input6, input7)
	return result == returns


def example2():
	cls = RandomColoringDiv2()
	input0 = 4
	input1 = 2
	input2 = 2
	input3 = 0
	input4 = 0
	input5 = 0
	input6 = 5
	input7 = 5
	returns = 0
	result = cls.getCount(input0, input1, input2, input3, input4, input5, input6, input7)
	return result == returns


def example3():
	cls = RandomColoringDiv2()
	input0 = 6
	input1 = 9
	input2 = 10
	input3 = 1
	input4 = 2
	input5 = 3
	input6 = 0
	input7 = 10
	returns = 540
	result = cls.getCount(input0, input1, input2, input3, input4, input5, input6, input7)
	return result == returns


def example4():
	cls = RandomColoringDiv2()
	input0 = 6
	input1 = 9
	input2 = 10
	input3 = 1
	input4 = 2
	input5 = 3
	input6 = 4
	input7 = 10
	returns = 330
	result = cls.getCount(input0, input1, input2, input3, input4, input5, input6, input7)
	return result == returns


def example5():
	cls = RandomColoringDiv2()
	input0 = 49
	input1 = 59
	input2 = 53
	input3 = 12
	input4 = 23
	input5 = 13
	input6 = 11
	input7 = 22
	returns = 47439
	result = cls.getCount(input0, input1, input2, input3, input4, input5, input6, input7)
	return result == returns



if __name__ == '__main__':
	print(example0()&example1()&example2()&example3()&example4()&example5())