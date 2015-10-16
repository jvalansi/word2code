from problem_utils import *


class SemiPerfectSquare:
    def check(self, N):
        input_int = N
        inf = 1000
        
        
        
        # Magical Girl Iris loves perfect squares.
        # A positive integer n is a perfect square if and only if there is a positive integer b >= 1 such that b*b = n. For example, 1 (=1*1), 16 (=4*4), and 169 (=13*13) are perfect squares, while 2, 54, and 48 are not.
        # Iris also likes semi-squares.
        # A positive integer n is called a semi-square if and only if there are positive integers a >= 1 and b > 1 such that a < b and a*b*b = n. For example, 81 (=1*9*9) and 48 (=3*4*4) are semi-squares, while 24, 63, and 125 are not.
        def reduce0(possibility):
            #### def reduce(possibility): return are(possibility)
            def reduce(possibility): return any(possibility)
            #### def mapping((a, b)): return ((a < b) and (((a * b) * b) == n))
            def mapping((a, b)): return ((a < b) and (((a * b) * b) == possibility))
            #### possibilities = combinations(range(n), 2)
            possibilities = combinations(range(possibility), 2)
            #### return(reduce(map(mapping, possibilities)))
            return reduce(map(mapping, possibilities))
        # (Note that we require that a < b.
        # Even though 24 can be written as 6*2*2, that does not make it a semi-square.)
        # You are given a int input_int .
        # Return "Yes" (quotes for clarity) if input_int is a semi-square number.
        #### possibilities = N
        possibilities = input_int
        #### reduce = lambda possibility: if(possibility, ["Yes", "No"])
        reduce = (lambda possibility: if_(possibility, ["Yes", "No"]))
        #### return reduce(semi_square(possibilities))
        return reduce(reduce0(possibilities))
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