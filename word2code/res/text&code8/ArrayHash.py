from problem_utils import * 
from operator import *
from string import lowercase, uppercase
import numpy


class ArrayHash:
    def getHash(self, input):
        input_array = numpy.array([list(element) for element in input])
        M,N = input_array.shape
        types = uppercase
        
        
        # You will be given a String[] input.
        # The value of each character in input is computed as follows:
        # Value = (Alphabet Position) + (Element of input) + (Position in Element)
        def mapping0(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = (lambda possibility: +(+(position(alphabet, input[Element[i]][Position[j]]), Element[i]), Position[j]))
            reduce = (lambda possibility: add(add(indexOf(types, input_array[possibility[0]][possibility[1]]), possibility[0]), possibility[1]))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # All positions are 0-based.
        # 'A' has alphabet position 0, 'B' has alphabet position 1, ...
        # The returned hash is the sum of all character values in input.
        #### possibilities = product(range(M),range(N))
        possibilities = product(range(M), range(N))
        #### def reduce(values): return sum(values)
        def reduce(possibility): return sum(possibility)
        #### returned(reduce(map(mapping0, input)))
        return reduce(map(mapping0, possibilities))
        # For example, if
        # input = {"CBA",
        # "DDD"}
        # then each character value would be computed as follows:
        # 2 =   2 + 0 + 0   :  'C' in element 0 position 0
        # 2 =   1 + 0 + 1   :  'B' in element 0 position 1
        # 2 =   0 + 0 + 2   :  'A' in element 0 position 2
        # 4  =  3 + 1 + 0   :  'D' in element 1 position 0
        # 5  =  3 + 1 + 1   :  'D' in element 1 position 1
        # 6  =  3 + 1 + 2   :  'D' in element 1 position 2
        # The final hash would be 2+2+2+4+5+6 = 21.

def example0():
    input = ["CBA", "DDD"]
    ah = ArrayHash()
    result = ah.getHash(input)
    returns = 21
    return returns == result

if __name__ == '__main__':
    print(example0())