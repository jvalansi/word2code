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
    velocities = [100]
    consumptions = [10000]
    fuel = 10000
    fc = FuelConsumption()
    result = fc.maximalDistance(velocities, consumptions, fuel)
    returns = 100.0
    return result == returns
    
if __name__ == '__main__':
    print(example0())