from utils import *
from operator import *

class MarbleDecoration:
    def maxLength(self, R, G, B):
        # Ash is a marble collector and he likes to create various ornaments using his marbles.
        
        # One day, Elsh asks him to create a simple decoration for her desk. 
        # She wants a sequence of marbles consisting of at most two different colors.
        #### valid1 = lambda sequence: at_most(len(different(sequence)), two)
        valid1 = lambda possibility: le(len(set(possibility)), 2)
        
        # To make the sequence look interesting, each pair of adjacent marbles must have different colors.
        #### valid2 = lambda marbles: each(different(* pair) for pair in adjacent(marbles))
        valid2 = lambda possibility: all(diff(* pair) for pair in cpairs(possibility))
        
        # Currently, Ash has R red marbles, G green marbles, and B blue marbles. 
        possibilities = transformations(['red']*R + ['green']*G + ['blue']*B)

        # Elsh wants that the resulting sequence is as long as possible. 
        # Return this maximum length.
        #### return(maximum(length(possibility) for possibility in possibilities if valid1(possibility) and valid2(possibility)))
        return(max(len(possibility) for possibility in possibilities if valid1(possibility) and valid2(possibility)))
    
    
if __name__ == '__main__':
    R = 3
    G = 0
    B = 0
    md = MarbleDecoration()
    print(md.maxLength(R, G, B))