
class GreatFairyWar:
    def minHP(self, dps, hp):
        input_array1 = dps
        input_array2 = hp
        N = len(dps)
        
        
        
        # You are a wizard.
        # You are facing N fairies, numbered 0 through N-1.
        # Your goal is to defeat all of them.
        # You can only attack one fairy at a time.
        # Moreover, you must fight the fairies in order: you can only attack fairy X+1 after you defeat fairy X.
        # On the other hand, all fairies that have not been defeated yet will attack you all the time.
        # Each fairy has two characteristics: her damage per second (input_array1) and her amount of hit points.
        # Your damage per second is 1.
        # That is, you are able to reduce an opponent's hit points by 1 each second.
        # In other words, if a fairy has H hit points, it takes you H seconds to defeat her.
        # You are given two int[]s, each of length N: input_array1 and input_array2.
        # For each i, input_array1[i] is the damage per second of fairy i, and input_array2[i] is her initial amount of hit points.
        def mapping0(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = lambda possibility: mul(dps[i], sum(hp[i:]))
            reduce = (lambda possibility: mul(input_array2[possibility], sum(input_array1[possibility:])))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # We assume that your number of hit points is sufficiently large to avoid defeat when fighting the fairies.
        # Compute and return the total number of hit points you'll lose during the fight.
        #### possibilities = range(N)
        possibilities = range(N)
        #### def reduce(possibility): return total(possibility)
        def reduce(possibility): return sum(possibility)
        #### return reduce(map(points, possibilities))
        return reduce(map(mapping0, possibilities))
        # In other words, return the total amount of damage the attacking fairies will deal.

def example0():
	cls = GreatFairyWar()
	input0 = [1,2]
	input1 = [3,4]
	returns = 17
	result = cls.minHP(input0, input1)
	return result == returns

def example1():
	cls = GreatFairyWar()
	input0 = [1,1,1,1,1,1,1,1,1,1]
	input1 = [1,1,1,1,1,1,1,1,1,1]
	returns = 55
	result = cls.minHP(input0, input1)
	return result == returns

def example2():
	cls = GreatFairyWar()
	input0 = [20,12,10,10,23,10]
	input1 = [5,7,7,5,7,7]
	returns = 1767
	result = cls.minHP(input0, input1)
	return result == returns

def example3():
	cls = GreatFairyWar()
	input0 = [5,7,7,5,7,7]
	input1 = [20,12,10,10,23,10]
	returns = 1998
	result = cls.minHP(input0, input1)
	return result == returns

def example4():
	cls = GreatFairyWar()
	input0 = [30,2,7,4,7,8,21,14,19,12]
	input1 = [2,27,18,19,14,8,25,13,21,30]
	returns = 11029
	result = cls.minHP(input0, input1)
	return result == returns

def example5():
	cls = GreatFairyWar()
	input0 = [1]
	input1 = [1]
	returns = 1
	result = cls.minHP(input0, input1)
	return result == returns

if __name__ == '__main__':
    print(example0())