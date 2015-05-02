from utils import *
from operator import *

class IdentifyingWood:
    def check(self, s, t):
        input_array0 = s
        input_array1 = t
        
        # We call a pair of Strings (s, t) "wood" if t is contained in s as a subsequence.
        #### wood = lambda s, t: contained(tuple(t), subsequence(s))
        valid = lambda possibility0, possibility1: contains(tuple(possibility1), csubsets(possibility0))

        # (See Notes for a formal definition.)
        
        # Given Strings s and t, return the String "Yep, it's wood." (quotes for clarity) if the pair (s, t) is wood and "Nope." otherwise.
        #### return "Yep, it's wood." if wood(s, t) otherwise "Nope."
        return "Yep, it's wood." if valid(input_array0, input_array1) else "Nope." 
 

if __name__ == '__main__':
    s = "absdefgh"
    t = "asdf"
    iw = IdentifyingWood()
    print(iw.check(s, t))