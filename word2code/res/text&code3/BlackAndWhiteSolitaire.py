from itertools import *
from utils import *
from operator import *

class BlackAndWhiteSolitaire:
    def minimumTurns(self,cardFront):
        input_array = list(cardFront)
        N = len(input_array)
        # Manao has N cards arranged in a sequence. 
        # He numbered them from left to right with numbers from 0 to N-1. 
        # Each card is colored black on one side and white on the other. 
        # Initially, each of the cards may lie on a different side. 
        # That is, some of the cards (possibly none or all of them) will be black side up and others will be white side up. 
        # Manao wants to flip some cards over to obtain an alternating configuration: every pair of successive cards must be of different colors.
        #### alternating = lambda cards: every([different(* pair) for pair in successive(cards)])
        valid = lambda possibility: all([diff(* pair) for pair in cpairs(possibility)]) 

        
        # You are given a String cardFront consisting of N characters. 
        # For each i, character i of cardFront is 'B' if card i lies black side up, and 'W' otherwise.
        elements = ['B','W']
        possibilities = product(elements,repeat=N)

        # Count and return the minimum number of cards which must be flipped to obtain an alternating configuration.
        #### return(minimum([flipped(input_array, possibility) for possibility in cards if alternating(possibility)]))
        return(min([len(diff(input_array, possibility)) for possibility in possibilities if valid(possibility)]))


if __name__ == '__main__':
    cardFront = "BBBW"
    baws = BlackAndWhiteSolitaire()
    print(baws.minimumTurns(cardFront))
