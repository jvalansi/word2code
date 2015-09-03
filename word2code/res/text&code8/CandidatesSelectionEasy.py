from operator import *


class CandidatesSelectionEasy:
    def sort(self, score, x):
        input_array = score
        input_int = x
        
        
        # Fox Ciel wants to hire a new maid.
        # There are n candidates for the position.
        # There are m different skills a maid should have, such as cooking, cleaning, or discreetness.
        # Ciel numbered the candidates 0 through n-1 and the skills 0 through m-1.
        # Ciel evaluated the level each candidate has in each of the skills.
        # You are given this information encoded in a String[] input_array with n elements, each consisting of m characters.
        # For each i and j, the character input_array[i][j] represents the level candidate i has in skill j.
        # Said character will always be between 'A' and 'Z', inclusive, where 'A' means the best possible and 'Z' the worst possible candidate.
        # You are also given an int input_int.
        # Ciel thinks that skill input_int is the most important skill a maid should have.
        # Return a int[] with n elements: the numbers of all candidates, ordered according to their level in skill input_int from the best to the worst.
        #### possibilities = ordered(input_array, according=itemgetter(x))
        possibilities = sorted(input_array, key=itemgetter(input_int))
        #### def mapping(possibility): return numbers(input_array, possibility)
        def mapping(possibility): return indexOf(input_array, possibility)
        #### return map(mapping, possibilities)
        return map(mapping, possibilities)

def example0():
    score = [[0,1],[2,0]]
    x = 1
    cse = CandidatesSelectionEasy()
    result = cse.sort(score, x) 
    returns = [1, 0]
    return result == returns
    
if __name__ == '__main__':
    print(example0())