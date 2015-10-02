from problem_utils import *


class FoxAndGame:
    def countStars(self, result):
        input_array = result
        N = len(input_array)
        
        
        # Fox Ciel is playing the popular game 'Cut the Rope' on her smartphone.
        # The game has multiple stages, and for each stage the player can gain between 0 and 3 stars, inclusive.
        # You are given a String[] input_array containing Fox Ciel's current results:
        # For each stage, input_array contains an element that specifies Ciel's input_array in that stage.
        # More precisely, input_array[i] will be "---" if she got 0 stars in stage i, "o--" if she got 1 star, "oo-" if she got 2 stars and "ooo" if she managed to get all 3 stars.
        def mapping0(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = lambda possibility: if(be(possibility, '---'), [0, if(be(possibility, 'o--'), [1, if(be(possibility, 'oo-'), [2, if(be(possibility, 'ooo'), [3, None])])])]))
            reduce = (lambda possibility: if_(is_(possibility, '---'), [0, if_(is_(possibility, 'o--'), [1, if_(is_(possibility, 'oo-'), [2, if_(is_(possibility, 'ooo'), [3, None])])])]))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # Return the total number of stars Ciel has at the moment.
        #### possibilities = input_array
        possibilities = input_array
        #### def reduce(possibility): return total(possibility)
        def reduce(possibility): return sum(possibility)
        #### return reduce(map(number, possibilities))
        return reduce(map(mapping0, possibilities))

def example0():
    result = ['ooo','ooo']
    fag = FoxAndGame()
    result = fag.countStars(result)
    returns = 6
    return result == returns
    
if __name__ == '__main__':
    print(example0())