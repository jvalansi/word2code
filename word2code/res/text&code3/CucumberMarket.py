from utils import *
from operator import *

class CucumberMarket:
    def check(self, price, budget, k):
        input_array = price
        input_int1 = budget
        input_int2 = k
        # Cucumber Boy is young and loves cucumbers.  
        # Therefore, Cucumber Boy will go to the cucumber market to buy some cucumbers.
        
        # Different cucumbers may have different costs.  
        # For each i, buying the i-th cucumber (0-based index) costs price[i] yen.
        
        # Cucumber Boy's mother gave him budget yen.  
        # However, he does not understand money well.
        # He just chooses some k unique cucumbers he likes.  
        #### possibilities = chooses(cucumbers, k)
        possibilities = subsets(input_array, input_int2)

        # If the total price of the chosen cucumbers is not greater than budget yen, he can buy them, otherwise he cannot.
        #### mapping = lambda possibility: not(greater(total(cucumbers), budget))
        mapping = lambda possibility: not_(gt(sum(possibility), input_int1))
        
        # You are given the int[] price, the int budget and the int k.  
    
        # Your method must return "YES" (quotes for clarity) if Cucumber Boy can buy any set of k unique cucumbers, and "NO" if there is some set of k cucumbers that is too expensive for him.
        #### return "YES" if any([can(set) for set in possibilities])  else "NO"
        return "YES" if all([mapping(possibility) for possibility in possibilities])  else "NO"

    
if __name__ == '__main__':
    price = [1000,1,10,100]
    budget = 1110
    k = 3
    cm = CucumberMarket()
    print(cm.check(price, budget, k))