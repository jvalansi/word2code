from problem_utils import *
from operator import *


class CucumberMarket:
    def check(self, price, budget, k):
        input_array = price
        input_int1 = budget
        input_int2 = k
        
        
        
        # Cucumber Boy is young and loves cucumbers.
        # Therefore, Cucumber Boy will go to the cucumber market to buy some cucumbers.
        # Different cucumbers may have different costs.
        # For each i, buying the i-th cucumber (0-based index) costs input_array[i] yen.
        # Cucumber Boy's mother gave him input_int1 yen.
        # However, he does not understand money well.
        # He just chooses some input_int2 unique cucumbers he likes.
        # If the total input_array of the chosen cucumbers is not greater than input_int1 yen, he can buy them, otherwise he cannot.
        def mapping0(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = (lambda possibility: not(greater(total(cucumbers), input_int1)))
            reduce = (lambda possibility: not_(gt(sum(possibility), input_int1)))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # You are given the int[] input_array, the int input_int1 and the int input_int2.
        # Your method must return "YES" (quotes for clarity) if Cucumber Boy can buy any set of input_int2 unique cucumbers, and "NO" if there is some set of input_int2 cucumbers that is too expensive for him.
        #### possibilities = set(cucumbers, input_int2)
        possibilities = subsets(input_array, input_int2)
        #### def reduce(possibility): return if(any(possibility), ['YES', 'NO'])
        def reduce(possibility): return if_(all(possibility), ['YES', 'NO'])
        #### return reduce(map(mapping0, possibilities))
        return reduce(map(mapping0, possibilities))

def example0():
	cls = CucumberMarket()
	input0 = [1000,1,10,100]
	input1 = 1110
	input2 = 3
	returns = "YES"
	result = cls.check(input0, input1, input2)
	return result == returns

def example1():
	cls = CucumberMarket()
	input0 = [1000,1,10,100]
	input1 = 1109
	input2 = 3
	returns = "NO"
	result = cls.check(input0, input1, input2)
	return result == returns

def example2():
	cls = CucumberMarket()
	input0 = [33,4]
	input1 = 33
	input2 = 1
	returns = "YES"
	result = cls.check(input0, input1, input2)
	return result == returns

def example3():
	cls = CucumberMarket()
	input0 = [1,1,1,1,1,1]
	input1 = 2
	input2 = 4
	returns = "NO"
	result = cls.check(input0, input1, input2)
	return result == returns

def example4():
	cls = CucumberMarket()
	input0 = [1000,1000,1000,1000,1000,1000,1000,1000,1000]
	input1 = 10000
	input2 = 9
	returns = "YES"
	result = cls.check(input0, input1, input2)
	return result == returns

if __name__ == '__main__':
    print(example0())