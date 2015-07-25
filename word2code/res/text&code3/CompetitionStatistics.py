from problem_utils import *
from operator import *

class CompetitionStatistics:
    def consecutiveGrowth(self, ratingChanges):
        input_array = ratingChanges
        N = len(input_array)
        possibilities = csubsets(input_array)
        # The longest consecutive rating increase streak is a very important statistic in any competition. 
        # You are to calculate this statistic for a certain player.
        # You will be given a int[] ratingChanges containing the rating changes of the player in chronological order. 

        # Your method should return the maximum number of consecutive competitions with positive rating changes.
        #### valid = lambda consecutive_competitions: all([positive(element, 0) for element in consecutive_competitions])
        valid = lambda possibility: all([gt(element, 0) for element in possibility])
        #### return(maximum([number(possibility) for possibility in consecutive(competitions) if valid(possibility)])) 
        return(max([len(possibility) for possibility in csubsets(input_array) if valid(possibility)])) 

        # Note that 0 is not a positive number.

if __name__ == '__main__':
    ratingChanges = [30, 5, -5, 3, 3, 1]
    cs = CompetitionStatistics()
    print(cs.consecutiveGrowth(ratingChanges))