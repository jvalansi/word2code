from problem_utils import *
from operator import *


class CompetitionStatistics:
    def consecutiveGrowth(self, ratingChanges):
        input_array = ratingChanges
        N = len(input_array)
        
        
        # The longest consecutive rating increase streak is a very important statistic in any competition.
        # You are to calculate this statistic for a certain player.
        # You will be given a int[] input_array containing the rating changes of the player in chronological order.
        # Your method should return the maximum number of consecutive competitions with positive rating changes.
        #### possibilities = consecutive(competitions)
        possibilities = csubsets(input_array)
        #### def mapping(possibility): return number(possibility)
        def mapping(possibility): return len(possibility)
        #### def valid(competitions): return all(map(positive ,competitions))
        def valid(possibility): return all(map(is_positive, possibility))
        #### def reduce(possibility): return maximum(possibility)
        def reduce(possibilities): return max(possibilities)
        #### return reduce(map(mapping, filter(valid, possibilities)))
        return reduce(map(mapping, filter(valid, possibilities)))
        # Note that 0 is not a positive number.

def example0():
    ratingChanges = [30, 5, -5, 3, 3, 1]
    cs = CompetitionStatistics()
    returns = 3
    result = cs.consecutiveGrowth(ratingChanges)
    return result == returns

if __name__ == '__main__':
    print(example0())