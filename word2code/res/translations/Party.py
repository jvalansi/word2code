from problem_utils import *

class Party:
    def averageNames(self, n, personA, personB):
        input_array0 = personA
        input_array1 = personB
        input_int = n
        # You are at a party where no one knows anyone else's name.
        # Each time two people shake hands, they introduce themselves to each other, and share with the other all the names they've learned at the party so far.
        def handshake(people):
            introduce(people)
            share(people, names)
        # You will be given an int n , the number of people at the party.
        # You will also be given a int[] personA and a int[] personB , containing the zero-based indices of the people who shook hands with each other, in chronological order.
        # Elements of personA and personB with equal indices describe the same handshake.
        # You should return the average number of names that each person at the party has learned, not including his or her own name.
        return(average(number(names)))



def example0():
	cls = Party()
	input0 = 4
	input1 = [0,1,2]
	input2 = [1,2,3]
	returns = 2.25
	result = cls.averageNames(input0, input1, input2)
	return result == returns


def example1():
	cls = Party()
	input0 = 5
	input1 = [0,0,0,0,0,0,0]
	input2 = [1,2,3,4,3,2,1]
	returns = 4.0
	result = cls.averageNames(input0, input1, input2)
	return result == returns


def example2():
	cls = Party()
	input0 = 100
	input1 = [52,19,52,19]
	input2 = [19,52,19,52]
	returns = 0.02
	result = cls.averageNames(input0, input1, input2)
	return result == returns


def example3():
	cls = Party()
	input0 = 25
	input1 = [14, 14, 16, 4, 14, 16, 2, 16, 8, 15, 17, 17, 3, 3, 19, 17, 20, 4, 24, 8]
	input2 = [16, 2, 23, 16, 11, 8, 5, 19, 15, 20, 19, 18, 14, 12, 22, 9, 0, 7, 23, 10]
	returns = 4.44
	result = cls.averageNames(input0, input1, input2)
	return result == returns



if __name__ == '__main__':
	print(example0())