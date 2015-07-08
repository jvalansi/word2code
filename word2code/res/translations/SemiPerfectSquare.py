from utils import *

class SemiPerfectSquare:
    def check(self, N):
        input_int = N
        inf = 1000
        # Magical Girl Iris loves perfect squares.
        # A positive integer n is a perfect square if and only if there is a positive integer b >= 1 such that b*b = n. For example, 1 (=1*1), 16 (=4*4), and 169 (=13*13) are perfect squares, while 2, 54, and 48 are not.
        # Iris also likes semi-squares.
        # A positive integer n is called a semi-square if and only if there are positive integers a >= 1 and b > 1 such that a < b and a*b*b = n. For example, 81 (=1*9*9) and 48 (=3*4*4) are semi-squares, while 24, 63, and 125 are not.
        # ROOT-0(root=called-6(nsubjpass=n-4(det=A-1, amod=positive-2, nn=integer-3), auxpass=is-5, dobj=semi-square-8(det=a-7), advcl=are-60(mark=if-9, cc=and-10, advmod=only-11, advcl=are-14(mark=if-12, expl=there-13, nsubj=integers-16(amod=positive-15, dep==-19(det=a-17, dep=>-18, dep=1-20, conj_and=b-22(dep=>-23), num=1-24, dep=such-25, prep_that=b-29(det=a-27, amod=<-28, conj_and=b-33(det=a-31, nn=*-32))), dep=n.-37(dep=*-34, nn=b-35, amod==-36, prep_for=example-39))), nsubj=81-41(dep==-43(rcmod=1-44(rcmod=9-46(dep=*-45), dep=*-47), dep=9-48), conj_and=48-51(prep=4-58(dep==-53, dep=3-54(dep=*-55), dep=4-56(dep=*-57)))), dep=semi-squares-61, advcl=are-70(mark=while-63, nsubj=24-64(conj_and=63-66, conj_and=125-69), neg=not-71))))
        are = any
        def semi_square(n): return are( a<b and a*b*b==n for a,b in combinations_with_replacement(range(n),2))
        # (Note that we require that a < b.
        # Even though 24 can be written as 6*2*2, that does not make it a semi-square.)
        # You are given a int N .
        # Return "Yes" (quotes for clarity) if N is a semi-square number.
        return "Yes" if semi_square(N) else "No"
        # Otherwise, return "No".



def example0():
	cls = SemiPerfectSquare()
	input0 = 48
	returns = "Yes"
	result = cls.check(input0)
	return result == returns


def example1():
	cls = SemiPerfectSquare()
	input0 = 1000
	returns = "No"
	result = cls.check(input0)
	return result == returns


def example2():
	cls = SemiPerfectSquare()
	input0 = 25
	returns = "Yes"
	result = cls.check(input0)
	return result == returns


def example3():
	cls = SemiPerfectSquare()
	input0 = 47
	returns = "No"
	result = cls.check(input0)
	return result == returns


def example4():
	cls = SemiPerfectSquare()
	input0 = 847
	returns = "Yes"
	result = cls.check(input0)
	return result == returns



if __name__ == '__main__':
	print(example0()&example1()&example2()&example3()&example4())