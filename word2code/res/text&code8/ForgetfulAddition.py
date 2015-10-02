from numpy import insert
from problem_utils import *


class ForgetfulAddition:
    def minNumber(self, expression):
        input_array = list(expression)
        N = len(expression)
        
        
        # Alice had two positive integers, a and b.
        # She typed the expression "a+b" into her computer, but the '+' key malfunctioned.
        # For example, instead of "128+9" the computer's screen now shows "1289".
        # Later, Bob saw the string on the screen.
        # He knows that the '+' sign is missing but he does not know where it belongs.
        # He now wonders what is the smallest possible result of Alice's original expression.
        # For example, if Bob sees the string "1289", Alice's expression is either "128+9" or "12+89" or "1+289".
        # These expressions evaluate to 137, 101, and 290.
        # The smallest of those three results is 101.
        # # You are given a String expression that contains the expression on Alice's screen.
        # # Compute and return the smallest possible result after inserting the missing plus sign
        # mapping = lambda possibility: eval(input_array[:possibility]+'+'+input_array[possibility:])
        # return(min(mapping(possibility) for possibility in possibilities))
        # You are given a String expression that contains the expression on Alice's screen.
        # Compute and return the smallest possible result after inserting the missing plus sign
        #### possibilities = range(N)
        possibilities = range(N)
        #### def mapping(possibility): return result(list2str(inserting(expression, possibility, plus)))
        def mapping(possibility): return eval(list2str(insert(input_array, possibility, '+')))
        #### def reduce(possibility): return smallest(possibility)
        def reduce(possibility): return min(possibility)
        #### return reduce(map(mapping, possibilities))
        return reduce(map(mapping, possibilities))

def example0():
    expression = '22'
    fa = ForgetfulAddition()
    result = fa.minNumber(expression)
    returns = 4
    return result == returns
    
if __name__ == '__main__':
    print(example0())