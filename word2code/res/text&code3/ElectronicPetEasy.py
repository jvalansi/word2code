class ElectronicPetEasy:
    def isDifficult(self, st1, p1, t1, st2, p2, t2):
        # Kirino has found a game in which she has to feed electronic pets.
        # There are two pets in the game.
        # You are given six ints st1,p1,t1,st2,p2,t2.
        # To win the game, Kirino must satisfy the following rules:
        
        # She must feed her first pet for the first time precisely at the time st1.
        # There must be exactly p1 seconds between any two consecutive feedings of the first pet.
        # She must feed the first pet exactly t1 times.
        # She must feed her second pet for the first time precisely at the time st2.
        # There must be exactly p2 seconds between any two consecutive feedings of the second pet.
        # She must feed the second pet exactly t2 times.
#         feed1 =  [0]*(st1-1) + ([1] + [0]*p1)*t1 
#         feed2 =  [0]*(st2-1) + ([1] + [0]*p2)*t2 
        
        # Feeding the pets is easy if Kirino never needs to feed both pets at the same time.
        # Return "Easy" (quotes for clarity) if feeding the pets is easy for the given inputs.
        # Otherwise, return "Difficult".
#         return "Easy" if not any(feed2[time] and feed1[time] for time in range(len(feed1))) else "Difficult"
        
        # Note that the return value is case-sensitive.


if __name__ == '__main__':
    [st1, p1, t1, st2, p2, t2] = [3,3,3,5,2,3]
    epe = ElectronicPetEasy()
    print(epe.isDifficult(st1, p1, t1, st2, p2, t2))