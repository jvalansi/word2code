from problem_utils import *
from operator import *
from string import lowercase


class ChangingString:
    def distance(self, A, B, K):
        input_array1 = A
        input_array2 = B
        input_int = K
        N = len(input_array1)
        types = lowercase
        
        
        # You are given two Strings input_array1 and input_array2 that have the same length and contain only types letters ('a'-'z').
        # The distance between two letters is defined as the absolute value of their difference.
        def mapping1(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = lambda possibility: absolute(difference(* letters))
            reduce = (lambda possibility: abs(sub(* possibility)))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # The distance between input_array1 and input_array2 is defined as the sum of the differences between each letter in input_array1 and the letter in input_array2 at the same position.
        def mapping0(possibility):
            #### possibilities = range(N)
            possibilities = range(N)
            #### def mapping(possibility0): return differences((ord(possibility[possibility0]), ord(input_array2[possibility0])))
            def mapping(possibility0): return mapping1((ord(possibility[possibility0]), ord(input_array2[possibility0])))
            #### def reduce(possibility): return sum(possibility)
            def reduce(possibility): return sum(possibility)
            #### return reduce(map(mapping, possibilities))
            return reduce(map(mapping, possibilities))
        # For example, the distance between "abcd" and "bcda" is 6 (1 + 1 + 1 + 3)
        # You must change exactly input_int characters in input_array1 into other types letters.
        def valid0(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = lambda possibility: exactly(len(change(A, characters)), K)
            reduce = (lambda possibility: eq(len(diff(input_array1, possibility)), input_int))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # Return the minimum possible distance between input_array1 and input_array2 after you perform that change.
        #### possibilities = product(elements,repeat = N)
        possibilities = product(types, repeat=N)
        #### def reduce(possibility): return minimum(possibility)
        def reduce(possibility): return min(possibility)
        #### return reduce(map(distance, filter(possible, possibilities)))
        return reduce(map(mapping0, filter(valid0, possibilities)))

def example0():
    A = "ab"
    B = "ba"
    K = 2
    cs = ChangingString()
    result = cs.distance(A, B, K)
    returns = 0
    return result == returns
    
if __name__ == '__main__':
    print(example0())