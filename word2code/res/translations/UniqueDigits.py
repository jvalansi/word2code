from utils import *

class UniqueDigits:
    def count(self, n):
        input_int = n
        inf = 10000
        integers = range(inf)
        # Given an int n find all positive integers less than n whose digits are all different.
        # ROOT-0(root=find-5(prep=Given-1(pobj=int-3(det=an-2)), nsubj=n-4, advmod=less-9(npadvmod=integers-8(det=all-6, amod=positive-7)), prep_than=n-11(rcmod=different-16(nsubj=digits-13(poss=whose-12), cop=are-14, advmod=all-15))))
        # root=find(nsubj=n, advmod=less(npadvmod=integers(det=all, amod=positive)), prep_than=n(rcmod=different(nsubj=digits(poss=whose), cop=are, advmod=all)))
        less_than = lt
        different = ne
        positive = is_positive
        def valid(integer): return positive(integer) and less_than(integer, n) and all(different(* digits) for digits in pairs(str(integer)))
        # Return the total number of such integers.
        # ROOT-0(root=Return-1(dep=number-4(det=the-2, amod=total-3, prep_of=integers-7(amod=such-6))))
        number = len
        such = valid
        return(number(filter(such, integers)))



def example0():
	cls = UniqueDigits()
	input0 = 21
	returns = 19
	result = cls.count(input0)
	return result == returns


def example1():
	cls = UniqueDigits()
	input0 = 101
	returns = 90
	result = cls.count(input0)
	return result == returns


def example2():
	cls = UniqueDigits()
	input0 = 1001
	returns = 738
	result = cls.count(input0)
	return result == returns


def example3():
	cls = UniqueDigits()
	input0 = 1
	returns = 0
	result = cls.count(input0)
	return result == returns



if __name__ == '__main__':
	print(example0()&example1()&example2()&example3())