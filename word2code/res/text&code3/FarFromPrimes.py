from utils import *

class FarFromPrimes:
    def count(self, A, B):
        input_int1 = A
        input_int2 = B
        # A prime number is an integer greater than 1 that has no positive divisors other than 1 and itself. 
        
        # The first prime numbers are 2, 3, 5, 7, 11, 13, 17, ...
        # The number N is considered far from primes if there are no prime numbers between N-10 and N+10, inclusive, i.e., all numbers N-10, N-9,  ..., N-1, N, N+1, ..., N+9, N+10 are not prime.
        #### far_from_primes = lambda N: no (number for number in between(N-10, inclusive(N+10)) if prime(number))
        valid = lambda N: not (i for i in range(N-10, inclusive(N+10)) if is_prime(i))

        # You are given an int A and an int B. 
        # Return the number of far from primes numbers between A and B, inclusive.
        #### return(number([numbers for numbers in between(A, inclusive(B)) if far_from_primes(numbers)]))
        return(len([i for i in range(input_int1, inclusive(input_int2)) if valid(i)]))
        
if __name__ == '__main__':
    A = 3328
    B = 4100
    ffp = FarFromPrimes()
    print(ffp.count(A, B))
