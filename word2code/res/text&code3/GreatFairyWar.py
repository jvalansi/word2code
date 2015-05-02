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
        
        # Each fairy has two characteristics: her damage per second (dps) and her amount of hit points.
        # Your damage per second is 1.
        # That is, you are able to reduce an opponent's hit points by 1 each second.
        # In other words, if a fairy has H hit points, it takes you H seconds to defeat her.
        
        # You are given two int[]s, each of length N: dps and hp.
        # For each i, dps[i] is the damage per second of fairy i, and hp[i] is her initial amount of hit points.
        mapping = lambda i: input_array2[i]*sum(input_array1[i:])

        # We assume that your number of hit points is sufficiently large to avoid defeat when fighting the fairies.
        # Compute and return the total number of hit points you'll lose during the fight.
        #### return(total(points(i) for i in range(N)))
        return(sum(mapping(i) for i in range(N)))
        
        # In other words, return the total amount of damage the attacking fairies will deal.
        
if __name__ == '__main__':
    dps = [1,2]
    hp = [3,4]
    gfw = GreatFairyWar()
    print(gfw.minHP(dps, hp))