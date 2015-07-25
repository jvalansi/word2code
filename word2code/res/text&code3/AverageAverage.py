from problem_utils import *

class AverageAverage:
    def average(self, numList):
        input_array = numList
        possibilities = subsets(input_array)

        # Given a int[] numList, for each non-empty subset of numList, compute the average of its elements, then return the average of those averages.
        #### return(average([average(subset) for subset of numList if subset]))
        return(average([average(possibility) for possibility in possibilities if possibility]))

    
if __name__ == '__main__':
    numList = [1,2,3]
    aa = AverageAverage()
    print(aa.average(numList))