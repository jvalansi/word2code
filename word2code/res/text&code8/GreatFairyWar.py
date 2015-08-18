
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
            #### reduce = lambda possibility: (dps[i] * sum(hp[i:]))
            reduce = (lambda possibility: (input_array2[possibility] * sum(input_array1[possibility:])))
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
    dps = [1,2]
    hp = [3,4]
    gfw = GreatFairyWar()
    result = gfw.minHP(dps, hp)
    returns = 17
    return result == returns
    
if __name__ == '__main__':
    print(example0())