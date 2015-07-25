from problem_utils import *
from operator import *

class LotteryTicket:
    def buy(self, price, b1, b2, b3, b4):
        input_array = [b1, b2, b3, b4]
        input_int = price
        # Nick likes to play the lottery.  
        # The cost of a single lottery ticket is price.  
        # Nick has exactly four banknotes with values b1, b2, b3 and b4 (some of the values may be equal).  
        # He wants to know if it's possible to buy a single lottery ticket without getting any change back.  
        # In other words, he wants to pay the exact price of a ticket using any subset of his banknotes.
        #### possibilities = subset(banknotes)
        possibilities = subsets(input_array)
        #### valid = any(exact(sum(subset), price) for subset of possibilities)  
        valid = any(eq(sum(possibility), input_int) for possibility in possibilities)  

        # Return "POSSIBLE" if it is possible or "IMPOSSIBLE" if it is not (all quotes for clarity).
        #### return "POSSIBLE" if possible or "IMPOSSIBLE"
        return "POSSIBLE" if valid else "IMPOSSIBLE"

    
if __name__ == '__main__':
    price = 10
    b1 = 1
    b2 = 5
    b3 = 10
    b4 = 50
    lt = LotteryTicket()
    print(lt.buy(price, b1, b2, b3, b4))