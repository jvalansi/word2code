from problem_utils import *
from operator import *

class MnemonicMemory:
    def getPhrase(self, number, dictionary):
        input_array1 = number
        input_array2 = dictionary
        N = len(input_array1)
        # It is often helpful to have a mnemonic phrase handy for a math test.  
        # For example, the number 25735 can be remembered as "is there anybody out there".  
        # If we count the number of characters in every word, we would get the sequence 2, 5, 7, 3, 5, which represents the original number!
        
        # Unfortunately for you, your professor likes to make the students memorize random numbers and then test them.  
        # To beat the system, your plan is to come up with mnemonic phrases that will represent the numbers you must memorize.
        
        # You are given a String number and a String[] dictionary.  
        # Return a single space delimited list of words, where each word is an element of dictionary, and no element of dictionary is used more than once. 
        possibilities = transformations(input_array2)
        mapping = lambda possibility: ' '.join(possibility)

        # The phrase must contain exactly n words, where n is the number of digits in the number, and the length of the i-th word must be equal to the i-th digit of the number for all i.
        #### valid = lambda possibility: exactly(len(phrase), n) and all(equal(length(phrase[i]), int(number[i])) for i in range(n))   
        valid = lambda possibility: eq(len(possibility), N) and all(eq(len(possibility[i]), int(input_array1[i])) for i in range(N))   
        
        # If more than one phrase is possible, return the one that comes first alphabetically (in other words, if you have several words of the same length, you should use them in alphabetical order).
        #### return(first(mapping(possibility) for possibility in possibilities if valid(possibility)))
        return(min(mapping(possibility) for possibility in possibilities if valid(possibility)))

if __name__ == '__main__':
    number = "25735"
    dictionary = ["is", "there", "anybody", "out", "there"]
    mm = MnemonicMemory()
    print(mm.getPhrase(number, dictionary))