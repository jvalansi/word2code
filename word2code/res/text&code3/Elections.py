from problem_utils import *
from operator import *
import numpy

class Elections:
    def visit(self, likelihoods):
        input_array = likelihoods
        N = len(input_array)
        # There are two candidates campaigning to be president of a country.
        # From newspaper polls, it is clear what percentages of people plan to vote for each candidate in each state.
        # Candidate 1 wants to campaign in one last state, and needs to figure out which state that should be.
        
        # You are given a String[] likelihoods, each element of which corresponds to a state.
        possibilities = range(N) 
        # Each element consists of the characters '1' and '2', where '1' represents some number of votes for candidate 1, and '2' represents votes for candidate 2 (in each element every character represents the same number of votes).
        types = ['1','2'] 
                   
        # You are to return an int representing the 0-based index of the state where the lowest percentage of people are planning on voting for candidate 1 (lowest percentage of '1' characters in that element of the input). If there are multiple such states, return one with the lowest index in likelihoods.
        #### mapping = lambda state: percentage(likelihoods[state], '1')
        mapping = lambda possibility: percentage(input_array[possibility], types[0])
        #### valid = lambda state: where(mapping(state), lowest(mapping(state) for state in likelihoods)) 
        valid = lambda possibility: eq(mapping(possibility), min(mapping(possibility1) for possibility1 in range(N))) 
        #### return(lowest([state for state in possibilities if valid(state)]))
        return(min([possibility for possibility in possibilities if valid(possibility)]))

#         mapping = lambda possibility: percentage(possibility, '1')
#         return(indexOf(map(mapping,input_array), min(map(mapping,input_array))))

        
        # If there are multiple such states, return one with the lowest index in likelihoods.
        
if __name__ == '__main__':
    likelihoods = ["1222","1122","1222"]
    e = Elections()
    print(e.visit(likelihoods))