from problem_utils import *
from operator import *


class LotteryTicket:
    def buy(self, price, b1, b2, b3, b4):
        input_array = [b1, b2, b3, b4]
        input_int = price
        
        
        # Nick likes to play the lottery.
        # The cost of a single lottery ticket is input_int.
        # Nick has exactly four banknotes with values b1, b2, b3 and b4 (some of the values may be equal).
        # He wants to know if it's possible to buy a single lottery ticket without getting any change back.
        # In other words, he wants to pay the exact input_int of a ticket using any subset of his banknotes.
        def reduce0(possibility):
            #### possibilities = subset(banknotes)
            possibilities = subsets(possibility)
            #### def mapping(possibility): return exact(sum(subset), input_int)
            def mapping(possibility): return eq(sum(possibility), input_int)
            #### def reduce(possibility): return any(possibility)
            def reduce(possibility): return any(possibility)
            #### return reduce(map(mapping, possibilities))
            return reduce(map(mapping, possibilities))
        # Return "POSSIBLE" if it is possible or "IMPOSSIBLE" if it is not (all quotes for clarity).
        #### possibilities = input_array
        possibilities = input_array
        #### reduce = lambda possibility: if(possibility, ['POSSIBLE', 'IMPOSSIBLE'])
        reduce = (lambda possibility: if_(possibility, ['POSSIBLE', 'IMPOSSIBLE']))
        #### return reduce(possible(possibilities))
        return reduce(reduce0(possibilities))

def example0():
    price = 10
    b1 = 1
    b2 = 5
    b3 = 10
    b4 = 50
    lt = LotteryTicket()
    result = lt.buy(price, b1, b2, b3, b4)
    returns = "POSSIBLE"
    return result == returns
    
if __name__ == '__main__':
    print(example0())