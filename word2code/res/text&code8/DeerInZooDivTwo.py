from problem_utils import *
from operator import *


class DeerInZooDivTwo:
    def getminmax(self, N, K):
        input_int1 = N
        input_int2 = K
        
        
        # Brus and Gogo came to the zoo today.
        # It's the season when deer shed their antlers.
        # There are input_int1 deer in the zoo.
        # Initially, each deer had exactly two antlers, but since then some deer may have lost one or both antlers.
        # (Now there may be some deer with two antlers, some with one, and some with no antlers at all.)
        # Brus and Gogo went through the deer enclosure and they collected all the antlers already lost by the deer.
        # The deer have lost exactly input_int2 antlers in total.
        def valid0(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = lambda possibility: exactly(sum(antlers), lost((2 * N), K))
            reduce = (lambda possibility: eq(sum(possibility), sub((2 * input_int1), input_int2)))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # Brus and Gogo are now trying to calculate how many deer have not lost any antlers yet.
        # Return a int[] with exactly two elements {x,y}, where x is the smallest possible number of deer that still have two antlers, and y is the largest possible number of those deer.
        #### possibilities = list(product(range(inclusive(2)), repeat=input_int1))
        possibilities = list(product(range(inclusive(2)), repeat=input_int1))
        #### def mapping(antlers): return number(antlers, two)
        def mapping(possibility): return countOf(possibility, 2)
        #### def reduce0(possibility): return smallest(possibility)
        def reduce0(possibility): return min(possibility)
        #### x = reduce0(map(mapping, filter(valid0, deer)))
        element0 = reduce0(map(mapping, filter(valid0, possibilities)))
        #### def reduce1(possibility): return largest(possibility)
        def reduce1(possibility): return max(possibility)
        #### y = reduce1(map(mapping, filter(valid0, deer)))
        element1 = reduce1(map(mapping, filter(valid0, possibilities)))
        #### return [x, y]
        return [element0, element1]

def example0():
    N = 3
    K = 2
    dizdt = DeerInZooDivTwo()
    result = dizdt.getminmax(N, K)
    returns = [1,2]
    return result == returns
    
if __name__ == '__main__':
    print(example0())