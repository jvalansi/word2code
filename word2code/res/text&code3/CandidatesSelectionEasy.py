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
        # You are given this information encoded in a String[] score with n elements, each consisting of m characters.
        # For each i and j, the character score[i][j] represents the level candidate i has in skill j.
        
        # Said character will always be between 'A' and 'Z', inclusive, where 'A' means the best possible and 'Z' the worst possible candidate.
        
        # You are also given an int x.
        # Ciel thinks that skill x is the most important skill a maid should have.
        
        # Return a int[] with n elements: the numbers of all candidates, ordered according to their level in skill x from the best to the worst.
        #### return([numbers(candidates, possibility) for possibility in ordered(candidates, skill(x))])
        return([indexOf(input_array, possibility) for possibility in sorted(input_array, itemgetter(input_int))])
