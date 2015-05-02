class FuelConsumption:
    def maximalDistance(self, velocities, consumptions, fuel):
        input_array1 = velocities
        input_array2 = consumptions
        input_int = fuel
        N = len(velocities)
        # You are taking your car on a long trip and have only a limited amount of fuel. 
        # You know how many liters of fuel your car uses per hour for certain speeds and you'd like to know how far a certain amount of fuel will take you when travelling at the optimal speed.
            
        # You will be given a int[] velocities and a int[] consumptions. 
        # velocities specifies a number of velocities in kilometers per hour. 
        # The ith element of consumptions is the amount of fuel (in milliliters) the car will consume in 1 hour, if your speed is equal to the ith element of velocities. 
        # In addition, you will be given an int fuel specifying the total amount of fuel in milliliters.
        # Your method should return a double, equal to the maximum distance that the car can travel (in kilometers) with the given amount of fuel, and travelling at a constant velocity equal to one of the elements of velocities.
        mapping = lambda possibility: input_array1[possibility] * float(input_int) / input_array2[possibility] 
        possibilities = range(N)
        #### return(maximum(distance(possibility) for possibility in possibilities))
        return(max(mapping(possibility) for possibility in possibilities))



if __name__ == '__main__':
    velocities = [100]
    consumptions = [10000]
    fuel = 10000
    fc = FuelConsumption()
    print(fc.maximalDistance(velocities, consumptions, fuel))