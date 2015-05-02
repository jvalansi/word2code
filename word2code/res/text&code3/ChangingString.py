from utils import *
from operator import *
from string import lowercase

class ChangingString:
    def distance(self, A, B, K):
        input_array1 = A
        input_array2 = B
        input_int = K
        N = len(input_array1)
        # You are given two Strings A and B that have the same length and contain only lowercase letters ('a'-'z').
        elements = lowercase
        possibilities = product(elements,repeat = N)
        
        # The distance between two letters is defined as the absolute value of their difference.
        #### distance = lambda letters: absolute(difference(* letters))
        mapping2 = lambda pair: abs(sub(* pair))


        # The distance between A and B is defined as the sum of the differences between each letter in A and the letter in B at the same position.
        #### distance = lambda A = sum([differences(A[position], B[position]) each position in range(N)])
        mapping = lambda possibility: sum([mapping2(possibility[i], input_array2[i]) for i in range(N)])
        # For example, the distance between "abcd" and "bcda" is 6 (1 + 1 + 1 + 3).
        
        # You must change exactly K characters in A into other lowercase letters.
        #### valid = lambda characters: exactly(len(change(A, characters)), K)
        valid = lambda possibility: eq(len(diff(input_array1, possibility)), input_int) 

        # Return the minimum possible distance between A and B after you perform that change.
        #### return(minimum([distance(A) for A in possibilities if possible(possibility)]))
        return(min([mapping(possibility) for possibility in possibilities if valid(possibility)]))
    
if __name__ == '__main__':
    A = "ab"
    B = "ba"
    K = 2
    cs = ChangingString()
    print(cs.distance(A, B, K))