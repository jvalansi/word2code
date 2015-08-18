from problem_utils import *
from operator import __eq__


class BasketsWithApples:
    def removeExcess(self, apples):
        input_array = apples
        
        
        # We have some baskets containing input_array, and we would like to perform the following procedure in a way that maximizes the number of remaining input_array.
        # First, we discard some (or none) of the baskets completely.
        # Then, if the remaining baskets do not all contain the same number of input_array, we remove excess input_array from the baskets until they do.
        def mapping0(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = lambda possibility: (len(possibility) * excess(possibility))
            reduce = (lambda possibility: (len(possibility) * min(possibility)))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # You will be given a int[] input_array where the i-th element of input_array is the number of input_array in the i-th basket.
        # Return the number of input_array remaining after the procedure described above is performed.
        #### possibilities = subsets(apples)
        possibilities = subsets(input_array)
        #### def reduce(possibility): return max(possibility)
        def reduce(possibility): return max(possibility)
        #### def valid(possibility): return possibility
        def valid(possibility): return possibility
        #### return reduce(map(mapping0, filter(valid, possibilities)))
        return reduce(map(mapping0, filter(valid, possibilities)))

def example0():
    apples = [1,2,3]
    bwa = BasketsWithApples()
    result = bwa.removeExcess(apples)
    returns = 4
    return result == returns
    
if __name__ == '__main__':
    print(example0())