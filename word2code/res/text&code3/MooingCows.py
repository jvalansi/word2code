from problem_utils import *

class MooingCows:
    def dissatisfaction(self, farmland):
        input_array = farmland
        # The cows in Byterland are mooing loudly, annoying the residents very much.  
        # Mrs. Darcy of the villa Pemberley is planning to resolve this problem by allowing only one cow to moo.  
        # She will pick the cow whose mooing is the least offensive to all the other cows.
        # The farmland in Pemberley is divided into n*m squares of grassland.  
        # Each square is either empty or occupied by a single cow.  
        # When a cow at (x,y) moos, the dissatisfaction of a cow at (i,j) is equal to the square of the distance between them: ((x-i)2 + (y-j)2).
        # The total dissatisfaction is the sum of the dissatisfaction of all the cows.
        
        # Return the minimal total dissatisfaction that can be achieved by allowing only a single cow to moo.
        distance = lambda element1, element2: 0 #TODO: fix
        possibilities = input_array  
        valid = lambda possibility: input_array[possibility] == 'C'
        mapping = lambda possibility: sum(distance(element, possibility) for element in farmland)
        #### return(minimal(total(dissatisfaction) for dissatisfaction in possibilities if valid(dissatisfaction)))
        return(min(mapping(possibility) for possibility in possibilities if valid(possibility)))
        # The farmland will be given as a String[], where '.' characters denote empty squares, and 'C' characters denote squares occupied by cows.
        