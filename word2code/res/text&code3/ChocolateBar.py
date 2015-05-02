from utils import *
from operator import *

class ChocolateBar:
    def maxLength(self, letters):
        input_array = letters
        possibilities = csubsets(input_array)
        # You just bought a very delicious chocolate bar from a local store. 
        # This chocolate bar consists of N squares, numbered 0 through N-1. 
        # All the squares are arranged in a single row. 
        # There is a letter carved on each square. 
        # You are given a String letters. 
        # The i-th character of letters denotes the letter carved on the i-th square (both indices are 0-based).
        
        # You want to share this delicious chocolate bar with your best friend. 
        # At first, you want to give him the whole bar, but then you remembered that your friend only likes a chocolate bar without repeated letters. 

        # Therefore, you want to remove zero or more squares from the beginning of the bar, and then zero or more squares from the end of the bar, in such way that the remaining bar will contain no repeated letters.
        #### valid = lambda bar: no [letters for letters contain pairs(bar) if repeated(* letters)]
        valid = lambda possibility: not [pair for pair in pairs(possibility) if eq(* pair)]
        filter
        # Return the maximum possible length of the remaining chocolate bar that contains no repeated letters.
        #### return(maximum(length(possibility) for possibility in csubsets(bar) if valid(possibility)))
        return(max(len(possibility) for possibility in csubsets(input_array) if valid(possibility)))
    
if __name__ == '__main__':
    letters = "dengklek"
    cb = ChocolateBar()
    print(cb.maxLength(letters))