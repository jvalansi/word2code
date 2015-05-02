from operator import *

class FoxAndGame:
    def countStars(self, result):
        input_array = result
        N = len(input_array)
        possibilities = input_array
        # Fox Ciel is playing the popular game 'Cut the Rope' on her smartphone.
        # The game has multiple stages, and for each stage the player can gain between 0 and 3 stars, inclusive.
    
        # You are given a String[] result containing Fox Ciel's current results:
        # For each stage, result contains an element that specifies Ciel's result in that stage.
        # More precisely, result[i] will be "---" if she got 0 stars in stage i, "o--" if she got 1 star, "oo-" if she got 2 stars and "ooo" if she managed to get all 3 stars.
        mapping = lambda possibility: countOf(possibility, 'o')
        # Return the total number of stars Ciel has at the moment.
        #### return(total(number(stars) for stars in possibilities))
        return(sum(mapping(possibility) for possibility in possibilities))

    
if __name__ == '__main__':
    result = ['ooo','ooo']
    fag = FoxAndGame()
    print(fag.countStars(result))