from problem_utils import *


class FarFromPrimes:
    def count(self, A, B):
        input_int1 = A
        input_int2 = B
        
        
        
        # input_int1 prime number is an integer greater than 1 that has no positive divisors other than 1 and itself.
        # The first prime numbers are 2, 3, 5, 7, 11, 13, 17, ...
        # The number N is considered far from primes if there are no prime numbers between N-10 and N+10, inclusive, i.e., all numbers N-10, N-9,  ..., N-1, N, N+1, ..., N+9, N+10 are not prime.
        def valid0(possibility):
            #### possibilities = numbers(N-10, inclusive(N+10))
            possibilities = range(possibility-10, inclusive(possibility+10))
            #### def valid(possibility): return prime(possibility)
            def valid(possibility): return is_prime(possibility)
            #### def reduce(possibility): return no(possibility)
            def reduce(possibility): return not_(possibility)
            #### return reduce(filter(valid, possibilities))
            return reduce(filter(valid, possibilities))
        # You are given an int input_int1 and an int input_int2.
        # Return the number of far from primes numbers between input_int1 and input_int2, inclusive.
        #### possibilities = numbers(input_int1, inclusive(input_int2))
        possibilities = range(input_int1, inclusive(input_int2))
        #### def reduce(possibility): return number(possibility)
        def reduce(possibility): return len(possibility)
        #### return reduce(filter(far_from_primes, possibilities))
        return reduce(filter(valid0, possibilities))

def example0():
	cls = FarFromPrimes()
	input0 = 3328
	input1 = 4100
	returns = 4
	result = cls.count(input0, input1)
	return result == returns

def example1():
	cls = FarFromPrimes()
	input0 = 10
	input1 = 1000
	returns = 0
	result = cls.count(input0, input1)
	return result == returns

def example2():
	cls = FarFromPrimes()
	input0 = 19240
	input1 = 19710
	returns = 53
	result = cls.count(input0, input1)
	return result == returns

def example3():
	cls = FarFromPrimes()
	input0 = 23659
	input1 = 24065
	returns = 20
	result = cls.count(input0, input1)
	return result == returns

def example4():
	cls = FarFromPrimes()
	input0 = 97001
	input1 = 97691
	returns = 89
	result = cls.count(input0, input1)
	return result == returns

if __name__ == '__main__':
    print(example0())