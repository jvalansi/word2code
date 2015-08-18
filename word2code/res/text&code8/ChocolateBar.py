from problem_utils import *
from operator import *


class ChocolateBar:
    def maxLength(self, letters):
        input_array = letters
        
        
        # You just bought a very delicious chocolate bar from a local store.
        # This chocolate bar consists of N squares, numbered 0 through N-1.
        # All the squares are arranged in a single row.
        # There is a letter carved on each square.
        # You are given a String input_array.
        # The i-th character of input_array denotes the letter carved on the i-th square (both indices are 0-based).
        # You want to share this delicious chocolate bar with your best friend.
        # At first, you want to give him the whole bar, but then you remembered that your friend only likes a chocolate bar without repeated input_array.
        # Therefore, you want to remove zero or more squares from the beginning of the bar, and then zero or more squares from the end of the bar, in such way that the remaining bar will contain no repeated input_array.
        def valid0(possibility):
            #### possibilities = pairs(bar)
            possibilities = pairs(possibility)
            #### def valid(letters): return repeated(* letters)
            def valid(possibility): return eq(*possibility)
            #### def reduce(possibility): return no(possibility)
            def reduce(possibility): return not_(possibility)
            #### return reduce(filter(valid, possibilities))
            return reduce(filter(valid, possibilities))
        # Return the maximum possible length of the remaining chocolate bar that contains no repeated input_array.
        #### possibilities = csubsets(bar)
        possibilities = csubsets(input_array)
        #### def mapping(possibility): return length(possibility)
        def mapping(possibility): return len(possibility)
        #### def reduce(possibility): return maximum(possibility)
        def reduce(possibility): return max(possibility)
        #### return reduce(map(mapping, filter(valid0, possibilities)))
        return reduce(map(mapping, filter(valid0, possibilities)))

def example0():
    letters = "dengklek"
    returns = 6
    cb = ChocolateBar()
    result = cb.maxLength(letters)
    return returns == result
        
if __name__ == '__main__':
    print(example0())