from utils import *

class TimeTravellingCellar:
    def determineProfit(self, profit, decay):
        input_array0 = profit
        input_array1 = decay
        N = len(profit)
        # Gogo owns N wine cellars, numbered 0 through N-1.
        # He possesses a time machine and will use it to advance time in one of the cellars, maturing all the wine inside.
        # However, as a side effect, he must also choose one other cellar and turn back time there, making the wine inside younger.
        # You are given two int[]s, profit and decay .
        # Advancing time in cellar i will gain Gogo a profit of profit [i].
        gain = sum
        def advancing_time(i): return gain(0,profit[i]) 
        # Turning back time in cellar i will lose him decay [i] in profit.
        lose = sub
        def turning_back_time(i): return lose(0,decay[i])
        # Return the maximum profit that Gogo can gain by advancing time in one cellar and turning time back in another cellar.
        # ROOT-0(root=Return-1(dobj=profit-4(det=the-2, nn=maximum-3, rcmod=gain-8(dobj=that-5, nsubj=Gogo-6, aux=can-7, prepc_by=advancing-10(dobj=time-11(prep_in=cellar-14(num=one-13)), conj_and=turning-16(dobj=time-17, advmod=back-18, prep_in=cellar-21(det=another-20)))))))
#         print([profit(one_cellar,another_cellar) for one_cellar, another_cellar in pairs(range(N))])
        maximum = max
        return(maximum(sum([advancing_time(one_cellar),turning_back_time(another_cellar)]) for one_cellar, another_cellar in pairs(range(N))))
        # It is guaranteed that this profit will be positive.



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