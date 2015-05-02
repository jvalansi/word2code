from operator import *

class MountainRanges:
    def countPeaks(self, heights):
        input_array = heights
        # Tom is in charge of a tourist agency.
        # He has a lovely picture of the local mountain range.
        # He would like to sell it to the tourists but first he needs to know how many peaks are visible in the picture.
        N = len(heights)
        
        # The mountain range in the picture can be seen as a sequence of heights.
        # You are given these heights as a int[] height.
        possibilities = range(N)
        # An element of height is called a peak if its value is strictly greater than each of the values of adjacent elements.
        valid = lambda possibility: all(heights[possibility] > heights[element] for element in possibilities if abs(possibility-element) == 1)
        
        # An element of height is called a peak if its value is strictly greater than each of the values of adjacent elements.
        #### peak = lambda element: each(greater(height[element], height[element]) for element in possibilities if adjacent(element, element))
        valid = lambda possibility: all(gt(input_array[possibility], input_array[element]) for element in possibilities if successive(possibility, element))

        # Compute and return the number of peaks in the given mountain range.
        #### return(number([possibility for possibility in possibilities if peaks(possibility)]))
        return(len([possibility for possibility in possibilities if valid(possibility)]))
    
if __name__ == '__main__':
    heights = [5, 6, 2, 4]
    cp = MountainRanges()
    print(cp.countPeaks(heights))
