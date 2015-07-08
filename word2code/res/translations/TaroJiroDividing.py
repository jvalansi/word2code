from utils import *

class TaroJiroDividing:
    def getNumber(self, A, B):
        input_int0 = A
        input_int1 = B
        # The dividing game is played as follows: You start by taking a clean sheet of paper and writing down some positive integer.
        # Then you repeat the following process: Let X be the last integer you wrote.
        while(True):
            X = last(integer)
        # If X is odd, the game ends.
            if is_odd(X): ends
        # Otherwise, divide X by 2 and write down the result.
            else: 
                write(divide(X,2))
        # For example, if you start the game by writing 12 you will then write 12/2 = 6, followed by 6/2 = 3, and as 3 is odd, the game ends there.
        # Your paper now contains the numbers 12, 6, and 3.
        # Cat Taro has just played the game starting with the integer A .
        # Jiro has also played the game but he started with the integer B .
        # You are given the ints A and B .
        # Return the number of integers that were written both by Taro and by Jiro.
        return(number(integers(written(Taro,Jiro))))



def example0():
	cls = TaroJiroDividing()
	input0 = 8
	input1 = 4
	returns = 3
	result = cls.getNumber(input0, input1)
	return result == returns


def example1():
	cls = TaroJiroDividing()
	input0 = 4
	input1 = 7
	returns = 0
	result = cls.getNumber(input0, input1)
	return result == returns


def example2():
	cls = TaroJiroDividing()
	input0 = 12
	input1 = 12
	returns = 3
	result = cls.getNumber(input0, input1)
	return result == returns


def example3():
	cls = TaroJiroDividing()
	input0 = 24
	input1 = 96
	returns = 4
	result = cls.getNumber(input0, input1)
	return result == returns


def example4():
	cls = TaroJiroDividing()
	input0 = 1000000000
	input1 = 999999999
	returns = 0
	result = cls.getNumber(input0, input1)
	return result == returns



if __name__ == '__main__':
	print(example0())