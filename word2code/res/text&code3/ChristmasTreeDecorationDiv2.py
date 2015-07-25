from problem_utils import *

class ChristmasTreeDecorationDiv2:
    def solve(self, col, x, y):
        input_array0 = col
        input_array1 = x
        input_array2 = y
        N = len(input_array1)
        # Christmas is just around the corner, and Alice just decorated her Christmas tree.
        # There are N stars and N-1 ribbons on the tree.
        # Each ribbon connects two of the stars in such a way that all stars and ribbons hold together.
        # (In other words, the stars and ribbons are the vertices and edges of a tree.)
        
        # The stars are numbered 1 through N.
        # Additionally, each star has some color.
        # You are given the colors of stars as a int[] col with N elements.
        # For each i, col[i] is the color of star i+1.
        # (Different integers represent different colors.)
        
        # You are also given a description of the ribbons: two int[]s x and y with N-1 elements each.
        # For each i, there is a ribbon that connects the stars with numbers x[i] and y[i].
        #### ribbon = [(x[i], y[i]) for i in range(N)]
        possibilities = [(input_array1[i], input_array2[i]) for i in range(N)]
        
        # According to Alice, a ribbon that connects two stars with different colors is beautiful, while a ribbon that connects two same-colored stars is not.
        #### beautiful = lambda ribbon: different(colors[stars[0]-1], colors[stars[1]-1]) 
        valid = lambda possibility: diff(input_array0[possibility[0]-1], input_array0[possibility[1]-1]) 
 
        # Compute and return the number of beautiful ribbons in Alice's tree.
        #### return(number([possibility for possibility in ribbons beautiful(possibility)]))
        return(len([possibility for possibility in possibilities if valid(possibility)]))
   
if __name__ == '__main__':
    col = [1,2,3,3]
    x = [1,2,3]
    y = [2,3,4]
    ctd = ChristmasTreeDecorationDiv2()
    print(ctd.solve(col, x, y))