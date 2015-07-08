from utils import *

class ShoutterDiv2:
    def count(self, s, t):
        input_array0 = s
        input_array1 = t
        # A group of freshman rabbits has recently joined the Eel club.
        # No two of the rabbits knew each other.
        # Today, each of the rabbits went to the club for the first time.
        # You are given int[]s s and t with the following meaning: For each i, rabbit number i entered the club at the time s [i] and left the club at the time t [i].
        # Each pair of rabbits that was in the club at the same time got to know each other, and they became friends on the social network service Shoutter.
        def friends(pair): same(time(pair))
        # This is also the case for rabbits who just met for a single moment (i.e., one of them entered the club exactly at the time when the other one was leaving).
        # Compute and return the number of pairs of rabbits that became friends today.
        # ROOT-0(root=Compute-1(conj_and=return-3(dobj=number-5(det=the-4, prep_of=pairs-7(prep_of=rabbits-9(rcmod=became-11(nsubj=that-10, xcomp=friends-12, tmod=today-13)))))))
        return(number(pairs(friends)))



def example0():
	cls = ShoutterDiv2()
	input0 = [1, 2, 4]
	input1 = [3, 4, 6]
	returns = 2
	result = cls.count(input0, input1)
	return result == returns


def example1():
	cls = ShoutterDiv2()
	input0 = [0]
	input1 = [100]
	returns = 0
	result = cls.count(input0, input1)
	return result == returns


def example2():
	cls = ShoutterDiv2()
	input0 = [0,0,0]
	input1 = [1,1,1]
	returns = 3
	result = cls.count(input0, input1)
	return result == returns


def example3():
	cls = ShoutterDiv2()
	input0 = [9,26,8,35,3,58,91,24,10,26,22,18,15,12,15,27,15,60,76,19,12,16,37,35,25,4,22,47,65,3,2,23,26,33,7,11,34,74,67,32,15,45,20,53,60,25,74,13,44,51]
	input1 = [26,62,80,80,52,83,100,71,20,73,23,32,80,37,34,55,51,86,97,89,17,81,74,94,79,85,77,97,87,8,70,46,58,70,97,35,80,76,82,80,19,56,65,62,80,49,79,28,75,78]
	returns = 830
	result = cls.count(input0, input1)
	return result == returns



if __name__ == '__main__':
	print(example0())