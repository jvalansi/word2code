from problem_utils import *
import string


class AverageAverage:
    def average(self, numList):
        input_array = numList
        
        
        
        # Given a int[] input_array, for each non-empty subset of input_array, compute the average of its elements, then return the average of those averages.
        #### possibilities = subset(numList)
        possibilities = subsets(input_array)
        #### def valid(possibility): return possibility
        def valid(possibility): return possibility
        #### def mapping(possibility): return average(possibility)
        def mapping(possibility): return average(possibility)
        #### def reduce(possibility): return average(possibility)
        def reduce(possibility): return average(possibility)
        #### return reduce(map(mapping, filter(valid, possibilities)))
        return reduce(map(mapping, filter(valid, possibilities)))

def example0():
    aa = AverageAverage()
    numList = [1,2,3]
    returns = 2.0
    result = aa.average(numList)
    return result == returns


if __name__ == '__main__':
    print(example0())