from problem_utils import *
from operator import *

class DeerInZooDivTwo:
    def getminmax(self, N, K):
        input_int1 = N
        input_int2 = K
        # Brus and Gogo came to the zoo today.
        # It's the season when deer shed their antlers.
        # There are N deer in the zoo.
        # Initially, each deer had exactly two antlers, but since then some deer may have lost one or both antlers.
        possibilities = list(product(range(inclusive(2)), repeat=input_int1))
        # (Now there may be some deer with two antlers, some with one, and some with no antlers at all.)
        
        # Brus and Gogo went through the deer enclosure and they collected all the antlers already lost by the deer.
 
        # The deer have lost exactly K antlers in total.
        #### valid = lambda antlers: exactly(sum(antlers), lost(2 * N, K))
        valid = lambda possibility: eq(sum(possibility), sub(2 * input_int1, input_int2))
        
        # Brus and Gogo are now trying to calculate how many deer have not lost any antlers yet.
        
        # Return a int[] with exactly two elements {x,y}, where x is the smallest possible number of deer that still have two antlers, and y is the largest possible number of those deer.
        #### x = smallest([number(antlers, two) for antlers in deer if valid(antlers)])
        element0 = min([countOf(possibility, 2) for possibility in possibilities if valid(possibility)])
        #### y = largest([number(antlers, two) for antlers in deer if valid(antlers)])
        element1 = max([countOf(possibility, 2) for possibility in possibilities if valid(possibility)])
        #### return ([x, y])
        return ([element0, element1])

if __name__ == '__main__':
    N = 3
    K = 2
    dizdt = DeerInZooDivTwo()
    print(dizdt.getminmax(N, K))