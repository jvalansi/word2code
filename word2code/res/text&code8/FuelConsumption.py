from problem_utils import *


class FuelConsumption:
    def maximalDistance(self, velocities, consumptions, fuel):
        input_array1 = velocities
        input_array2 = consumptions
        input_int = fuel
        N = len(velocities)
        
        
        
        # You are taking your car on a long trip and have only a limited amount of input_int.
        # You know how many liters of input_int your car uses per hour for certain speeds and you'd like to know how far a certain amount of input_int will take you when travelling at the optimal speed.
        # You will be given a int[] input_array1 and a int[] input_array2.
        # input_array1 specifies a number of input_array1 in kilometers per hour.
        # The ith element of input_array2 is the amount of input_int (in milliliters) the car will consume in 1 hour, if your speed is equal to the ith element of input_array1.
        # In addition, you will be given an int input_int specifying the total amount of input_int in milliliters.
        # Your method should return a double, equal to the maximum distance that the car can travel (in kilometers) with the given amount of input_int, and travelling at a constant velocity equal to one of the elements of input_array1.
        #### def mapping(possibility): return div(mul(input_array1[possibility], float(input_int)), input_array2[possibility])
        def mapping(possibility): return div(mul(input_array1[possibility], float(input_int)), input_array2[possibility])
        #### possibilities = range(N)
        possibilities = range(N)
        #### def reduce(possibility): return maximum(possibility)
        def reduce(possibility): return max(possibility)
        #### return reduce(map(distance, possibilities))
        return reduce(map(mapping, possibilities))

def example0():
	cls = FuelConsumption()
	input0 = [100]
	input1 = [10000]
	input2 = 10000
	returns = 100.0
	result = cls.maximalDistance(input0, input1, input2)
	return result == returns

def example1():
	cls = FuelConsumption()
	input0 = [70, 80, 90, 100, 60, 110]
	input1 = [4000, 4000, 4000, 4000, 4000, 4000]
	input2 = 40000
	returns = 1100.0
	result = cls.maximalDistance(input0, input1, input2)
	return result == returns

def example2():
	cls = FuelConsumption()
	input0 = [250, 240, 230, 220, 210, 211]
	input1 = [5000, 4500, 4000, 3500, 3000, 3000]
	input2 = 50000
	returns = 3516.6666666666665
	result = cls.maximalDistance(input0, input1, input2)
	return result == returns

def example3():
	cls = FuelConsumption()
	input0 = [5, 10, 20, 40, 80]
	input1 = [1000, 2500, 6250, 9000, 18000]
	input2 = 47832
	returns = 239.16
	result = cls.maximalDistance(input0, input1, input2)
	return result == returns

def example4():
	cls = FuelConsumption()
	input0 = [5, 10, 20, 40, 80, 160]
	input1 = [1000, 2500, 6250, 8000, 9500, 20000]
	input2 = 47832
	returns = 402.79578947368424
	result = cls.maximalDistance(input0, input1, input2)
	return result == returns

def example5():
	cls = FuelConsumption()
	input0 = [240, 195, 130, 133, 15, 160, 111, 206, 72, 149, 146, 115, 235, 183, 102, 96, 163, 61, 196, 52, 87, 139, 33, 7, 90, 67, 118, 227, 197, 114]
	input1 = [14837, 2981, 17292, 18591, 4832, 7461, 17991, 18369, 18291, 9400, 15179, 3317, 2595, 2441, 6936, 8028, 14973, 18981, 12503, 7816, 2883, 6385, 6230, 18157, 16567, 9310, 2866, 4687, 14171, 4477]
	input2 = 31710
	returns = 2871.6184971098264
	result = cls.maximalDistance(input0, input1, input2)
	return result == returns

if __name__ == '__main__':
    print(example0())