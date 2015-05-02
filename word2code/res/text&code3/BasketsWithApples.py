from utils import *
from operator import __eq__

class BasketsWithApples:
    def removeExcess(self, apples):
        input_array = apples
        # We have some baskets containing apples, and we would like to perform the following procedure in a way that maximizes the number of remaining apples.  
        # First, we discard some (or none) of the baskets completely.  
        possibilities = subsets(input_array)

        # Then, if the remaining baskets do not all contain the same number of apples, we remove excess apples from the baskets until they do.
#         valid = lambda possibility: all(__eq__(pair) for pair in subsets(possibility, 2))
        mapping = lambda possibility: len(possibility) * min(possibility) 
        
        # You will be given a int[] apples where the i-th element of apples is the number of apples in the i-th basket.
        
        # Return the number of apples remaining after the procedure described above is performed.
        #### return(max([number(possibility) for possibility in apples]))
        return(max([mapping(possibility) for possibility in possibilities]))

    
if __name__ == '__main__':
    apples = [1,2,3]
    bwa = BasketsWithApples()
    print(bwa.removeExcess(apples))