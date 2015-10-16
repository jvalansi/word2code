from operator import *


class CandidatesSelectionEasy:
    def sort(self, score, x):
        input_array = score
        input_int = x
        
        
        
        # Fox Ciel wants to hire a new maid.
        # There are n candidates for the position.
        # There are m different skills a maid should have, such as cooking, cleaning, or discreetness.
        # Ciel numbered the candidates 0 through n-1 and the skills 0 through m-1.
        # Ciel evaluated the level each candidate has in each of the skills.
        # You are given this information encoded in a String[] input_array with n elements, each consisting of m characters.
        # For each i and j, the character input_array[i][j] represents the level candidate i has in skill j.
        # Said character will always be between 'A' and 'Z', inclusive, where 'A' means the best possible and 'Z' the worst possible candidate.
        # You are also given an int input_int.
        # Ciel thinks that skill input_int is the most important skill a maid should have.
        # Return a int[] with n elements: the numbers of all candidates, ordered according to their level in skill input_int from the best to the worst.
        #### possibilities = ordered(input_array, according=itemgetter(x))
        possibilities = sorted(input_array, key=itemgetter(input_int))
        #### def mapping(possibility): return numbers(input_array, possibility)
        def mapping(possibility): return indexOf(input_array, possibility)
        #### return map(mapping, possibilities)
        return map(mapping, possibilities)

def example0():
	cls = CandidatesSelectionEasy()
	input0 = ["ACB", "BAC", "CBA"]
	input1 = 1
	returns = [1, 2, 0 ]
	result = cls.sort(input0, input1)
	return result == returns

def example1():
	cls = CandidatesSelectionEasy()
	input0 = ["A", "C", "B", "C", "A"]
	input1 = 0
	returns = [0, 4, 2, 1, 3 ]
	result = cls.sort(input0, input1)
	return result == returns

def example2():
	cls = CandidatesSelectionEasy()
	input0 = ["LAX","BUR","ONT","LGB","SAN","SNA","SFO","OAK","SJC"]
	input1 = 2
	returns = [5, 3, 8, 7, 4, 6, 1, 2, 0 ]
	result = cls.sort(input0, input1)
	return result == returns

def example3():
	cls = CandidatesSelectionEasy()
	input0 = ["BBCBABAC","BCBACABA","CCCBAACB","CACABABB","AABBBBCC"]
	input1 = 6
	returns = [0, 1, 3, 2, 4 ]
	result = cls.sort(input0, input1)
	return result == returns

def example4():
	cls = CandidatesSelectionEasy()
	input0 = ["XXYWZWWYXZ","YZZZYWYZYW","ZYZZWZYYWW","ZWZWZWZXYW","ZYXWZXWYXY","YXXXZWXWXW","XWWYZWXYXY","XYYXYWYXWY","ZZYXZYZXYY","WXZXWYZWYY"]
	input1 = 3
	returns = [0, 3, 4, 5, 7, 8, 9, 6, 1, 2 ]
	result = cls.sort(input0, input1)
	return result == returns

def example5():
	cls = CandidatesSelectionEasy()
	input0 = ["X"]
	input1 = 0
	returns = [0 ]
	result = cls.sort(input0, input1)
	return result == returns

if __name__ == '__main__':
    print(example0())