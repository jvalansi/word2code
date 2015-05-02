from utils import *
from operator import *

class FoxAndFlowerShopDivTwo:
    def theMaxFlowers(self, flowers, r, c):
        input_array = numpy.array(list(element) for element in flowers)
        input_int1 = r
        input_int2 = c
        # Fox Jiro came to a flower shop to buy flowers.
        # The flowers in the shop are arranged in some cells of a rectangular grid.
        # The layout of the grid is given as a String[] flowers.
        # If the j-th cell of the i-th row of the grid contains a flower, then the j-th character of the i-th element of flowers will be 'F'.
        # (All indices in the previous sentence are 0-based.)
        # If the particular cell is empty, the corresponding character will be '.' (a period).
        types = ['F','.']
        
        # In order to buy flowers, Jiro has to draw a rectangle on this grid and buy all the flowers which lie inside the rectangle.
        # Of course, the sides of the rectangle must be on cell boundaries.
        possibilities = csubsets(input_array)
        # (Therefore, the sides of the rectangle will necessarily be parallel to the coordinate axes.)
        
        # Jiro wants to buy as many flowers as possible.
        # Unfortunately, he cannot select the entire grid.
        # Eel Saburo came to this shop before Jiro.
        # Saburo has already drawn his rectangle.
        # Saburo's rectangle contains just a single cell: the c-th cell of the r-th row of the grid.
        input_array[input_int1][input_int2] = 'C'
        # (Again, both indices are 0-based.)
        # Jiro's rectangle may not contain this cell.
        valid = lambda possibility: 'C' not in possibility 
        
        # Jiro's rectangle may not contain this cell.
        #### valid = lambda rectangle: not(contain(rectangle, cell)) 
        valid = lambda possibility: not_(contains(possibility, element)) 
        
        # You are given the String[] flowers and the ints r and c.
        # Return the maximum possible number of flowers Jiro can buy in this situation.
        #### return(maximum(number(possibility, flowers[0]) for possibility in possibilities if valid(possibility)))
        return(max(countOf(possibility, types[0]) for possibility in possibilities if valid(possibility)))


if __name__ == '__main__':
    flowers = ["F.F", ".F.", ".F."]
    r = 1
    c = 1
    fafsd2 = FoxAndFlowerShopDivTwo()
    print(fafsd2.theMaxFlowers(flowers, r, c))