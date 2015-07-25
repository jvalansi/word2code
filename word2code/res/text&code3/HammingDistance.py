from problem_utils import *
from operator import *

class HammingDistance:
    def minDistance(self, numbers):
        input_array = numbers
        N = len(input_array[0])
        
        # The Hamming distance between two numbers is defined as the number of positions in their binary representations at which they differ (leading zeros are used if necessary to make the binary representations have the same length) -
        #### hamming_distance = lambda numbers: number(differ(numbers[0][positions], numbers[1][positions]) for positions in range(N)) 
        mapping = lambda numbers: len(ne(numbers[0][i], numbers[1][i]) for i in range(N)) 

        # e.g., the numbers "11010" and "01100" differ at the first, third and fourth positions, so they have a Hamming distance of 3.
            
        # You will be given a String[] numbers containing the binary representations of some numbers (all having the same length). 
        # You are to return the minimum among the Hamming distances of all pairs of the given numbers.
        #### return(minimum(hamming_distances(possibility) for possibility in pairs(numbers)))
        return(min(mapping(possibility) for possibility in pairs(input_array)))

        
if __name__ == '__main__':
    numbers = ["11010", "01100"]
    hd = HammingDistance()
    print(hd.minDistance(numbers))