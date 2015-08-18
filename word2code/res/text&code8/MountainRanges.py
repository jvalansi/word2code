from problem_utils import *


class MountainRanges:
    def countPeaks(self, heights):
        input_array = heights
        N = len(heights)
        
        
        # Tom is in charge of a tourist agency.
        # He has a lovely picture of the local mountain range.
        # He would like to sell it to the tourists but first he needs to know how many peaks are visible in the picture.
        # The mountain range in the picture can be seen as a sequence of input_array.
        # You are given these input_array as a int[] height.
        # An element of height is called a peak if its value is strictly greater than each of the values of adjacent elements.
        # valid = lambda possibility: all(input_array[possibility] > input_array[element] for element in possibilities if abs(possibility-element) == 1)
        # An element of height is called a peak if its value is strictly greater than each of the values of adjacent elements.
        def valid0(possibility):
            #### def valid(possibility0): return adjacent([possibility, possibility0])
            def valid(possibility0): return successive([possibility, possibility0])
            #### def mapping(possibility0): return greater(value[possibility], value[possibility0])
            def mapping(possibility0): return gt(input_array[possibility], input_array[possibility0])
            #### def reduce(possibility): return each(possibility)
            def reduce(possibility): return all(possibility)
            #### return reduce(map(mapping, filter(valid, elements)))
            return reduce(map(mapping, filter(valid, possibilities)))
        # Compute and return the number of peaks in the given mountain range.
        #### possibilities = range(N)
        possibilities = range(N)
        #### def reduce(possibility): return number(possibility)
        def reduce(possibility): return len(possibility)
        #### return reduce(filter(valid0, possibilities))
        return reduce(filter(valid0, possibilities))

def example0():
    heights = [5, 6, 2, 4]
    cp = MountainRanges()
    result = cp.countPeaks(heights)
    returns = 2
    return result == returns
    
if __name__ == '__main__':
    print(example0())