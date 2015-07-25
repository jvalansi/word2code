from problem_utils import * 
from operator import *
from string import lowercase, uppercase
import numpy

class ArrayHash:
    def getHash(self, input):
        input_array = numpy.array([list(element) for element in input])
        M,N = input_array.shape
        possibilities = product(range(M),range(N))
        # You will be given a String[] input.  

        # The value of each character in input is computed as follows:
        #   Value = (Alphabet Position) + (Element of input) + (Position in Element)
        #### value = lambda (i, j): position(alphabet, input[i][j]) + i + j 
        mapping = lambda (i, j): indexOf(types, input_array[i][j]) + i + j   

        
        # All positions are 0-based.  
        # 'A' has alphabet position 0, 'B' has alphabet position 1, ... 
        types = uppercase

        # The returned hash is the sum of all character values in input.
        #### returned(sum([values(character) for character in input]))
        return(sum([mapping(possibility) for possibility in possibilities])) 
        
        # For example, if 
        # input = {"CBA",
        #         "DDD"}
        # then each character value would be computed as follows: 
        # 2 =   2 + 0 + 0   :  'C' in element 0 position 0
        # 2 =   1 + 0 + 1   :  'B' in element 0 position 1
        # 2 =   0 + 0 + 2   :  'A' in element 0 position 2
        # 4  =  3 + 1 + 0   :  'D' in element 1 position 0
        # 5  =  3 + 1 + 1   :  'D' in element 1 position 1
        # 6  =  3 + 1 + 2   :  'D' in element 1 position 2
        # The final hash would be 2+2+2+4+5+6 = 21.
        
if __name__ == '__main__':
    input = ["CBA", "DDD"]
    ah = ArrayHash()
    print(ah.getHash(input))