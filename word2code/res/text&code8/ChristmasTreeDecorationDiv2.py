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
        # You are given the colors of stars as a int[] input_array0 with N elements.
        # For each i, input_array0[i] is the color of star i+1.
        # (Different integers represent different colors.)
        # You are also given a description of the ribbons: two int[]s input_array1 and input_array2 with N-1 elements each.
        # For each i, there is a ribbon that connects the stars with numbers input_array1[i] and input_array2[i].
        #### possibilities = connects(input_array1,input_array2)
        possibilities = zip(input_array1,input_array2)
        # According to Alice, a ribbon that connects two stars with different colors is beautiful, while a ribbon that connects two same-colored stars is not.
        def valid0(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = lambda possibility: different(colors[(stars[0] - 1)], colors[(stars[1] - 1)])
            reduce = (lambda possibility: ne(input_array0[(possibility[0] - 1)], input_array0[(possibility[1] - 1)]))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # Compute and return the number of beautiful ribbons in Alice's tree.
        #### def reduce(possibility): return number(possibility)
        def reduce(possibility): return len(possibility)
        #### return reduce(filter(valid0, possibilities))
        return reduce(filter(valid0, possibilities))

def example0():
	cls = ChristmasTreeDecorationDiv2()
	input0 = [1,2,3,3]
	input1 = [1,2,3]
	input2 = [2,3,4]
	returns = 2
	result = cls.solve(input0, input1, input2)
	return result == returns

def example1():
	cls = ChristmasTreeDecorationDiv2()
	input0 = [1,3,5]
	input1 = [1,3]
	input2 = [2,2]
	returns = 2
	result = cls.solve(input0, input1, input2)
	return result == returns

def example2():
	cls = ChristmasTreeDecorationDiv2()
	input0 = [1,1,3,3]
	input1 = [1,3,2]
	input2 = [2,1,4]
	returns = 2
	result = cls.solve(input0, input1, input2)
	return result == returns

def example3():
	cls = ChristmasTreeDecorationDiv2()
	input0 = [5,5,5,5]
	input1 = [1,2,3]
	input2 = [2,3,4]
	returns = 0
	result = cls.solve(input0, input1, input2)
	return result == returns

def example4():
	cls = ChristmasTreeDecorationDiv2()
	input0 = [9,1,1]
	input1 = [3,2]
	input2 = [2,1]
	returns = 1
	result = cls.solve(input0, input1, input2)
	return result == returns

if __name__ == '__main__':
    print(example0())