from utils import *
from operator import *

class EggCartons:
    def minCartons(self, n):
        input_int = n
        # There are two types of egg cartons. 
        # One type contains 6 eggs and the other type contains 8 eggs.
        elements = [6,8]
        possibilities = subsets(elements*n)

        # John wants to buy exactly n eggs.
        #### valid = lambda eggs: exactly(sum(eggs), n)
        valid = lambda possibility: eq(sum(possibility), input_int)

        # Return the minimal number of egg cartons he must buy.
        #### return(minimal([number(egg_cartons) for egg_cartons in possibilities if valid(egg_cartons)])) 
        return(min([len(possibility) for possibility in possibilities if valid(possibility)])) 

        # If it's impossible to buy exactly n eggs, return -1.\
#         if possible else -1

if __name__ == '__main__':
    n = 24
    ec = EggCartons()
    print(ec.minCartons(n))