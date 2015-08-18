from operator import *


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
            #### reduce = lambda possibility: (0 if be(i, '---') else (1 if be(i, 'o--') else (2 if be(i, 'oo-') else (3 if be(i, 'ooo') else None))))
            reduce = (lambda possibility: (0 if is_(possibility, '---') else (1 if is_(possibility, 'o--') else (2 if is_(possibility, 'oo-') else (3 if is_(possibility, 'ooo') else None)))))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # Return the total number of stars Ciel has at the moment.
        #### possibilities = input_array
        possibilities = input_array
        #### def reduce(possibility): return sum(possibility)
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