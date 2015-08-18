from problem_utils import *


class TimeTravellingCellar:
    def determineProfit(self, profit, decay):
        input_array0 = profit
        input_array1 = decay
        N = len(profit)
        
        
        
        # Gogo owns N wine cellars, numbered 0 through N-1.
        # He possesses a time machine and will use it to advance time in one of the cellars, maturing all the wine inside.
        # However, as a side effect, he must also choose one other cellar and turn back time there, making the wine inside younger.
        # You are given two int[]s, input_array0 and input_array1 .
        # Advancing time in cellar i will gain Gogo a input_array0 of input_array0 [i].
        def advancing_time(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = lambda possibility: gain(0, profit[possibility])
            reduce = (lambda possibility: add(0, profit[possibility]))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # Turning back time in cellar i will lose him input_array1 [i] in input_array0.
        def turning_back_time(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = lambda possibility: lose(0, decay[possibility])
            reduce = (lambda possibility: sub(0, decay[possibility]))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # Return the maximum input_array0 that Gogo can gain by advancing time in one cellar and turning time back in another cellar.
        # print([input_array0(one_cellar,another_cellar) for one_cellar, another_cellar in pairs(range(N))])
        #### def reduce(possibility): return maximum(possibility)
        def reduce(possibility): return max(possibility)
        #### def mapping((one_cellar, another_cellar)): return sum([advancing_time(one_cellar), turning_back_time(another_cellar)])
        def mapping((one_cellar, another_cellar)): return sum([advancing_time(one_cellar), turning_back_time(another_cellar)])
        #### possibilities = pairs(range(N))
        possibilities = pairs(range(N))
        #### return reduce(map(mapping, possibilities))
        return reduce(map(mapping, possibilities))
        # It is guaranteed that this input_array0 will be positive.

def example0():
	cls = TimeTravellingCellar()
	input0 = [1,2,3]
	input1 = [3,1,2]
	returns = 2
	result = cls.determineProfit(input0, input1)
	return result == returns


def example1():
	cls = TimeTravellingCellar()
	input0 = [3,2]
	input1 = [1,2]
	returns = 1
	result = cls.determineProfit(input0, input1)
	return result == returns


def example2():
	cls = TimeTravellingCellar()
	input0 = [3,3,3]
	input1 = [1,1,1]
	returns = 2
	result = cls.determineProfit(input0, input1)
	return result == returns


def example3():
	cls = TimeTravellingCellar()
	input0 = [1000,500,250,125]
	input1 = [64,32,16,8]
	returns = 992
	result = cls.determineProfit(input0, input1)
	return result == returns



if __name__ == '__main__':
	print(example0()&example1()&example2()&example3())