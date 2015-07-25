from problem_utils import *

class SquareScoresDiv2:
    def getscore(self, s):
        input_array = s
        # A substring of a string is a contiguous sequence of characters from the string.
        contiguous_sequence = csubsets
        def substrings(string): return contiguous_sequence(string)
        # For example, each of the strings "ab", "bcd", and "e" is a substring of "abcde".
        # On the other hand, "cba", "ace", and "f" are not substrings of "abcde".
        # The score of a string S is the number of ways in which we can select a non-empty substring of S such that all characters in the substring are the same.
        # ROOT-0(root=number-9(nsubj=score-2(det=The-1, prep_of=S-6(det=a-4, nn=string-5)), cop=is-7, det=the-8, prep_of=ways-11(rcmod=select-16(prep_in=which-13, nsubj=we-14, aux=can-15, dobj=substring-19(det=a-17, amod=non-empty-18, prep_of=S-21), prep=such-22, ccomp=same-31(mark=that-23, nsubj=characters-25(det=all-24, prep_in=substring-28(det=the-27)), cop=are-29, det=the-30)))))
        # is(score(S),number(select(substring,S),same(charactes,all,substring))
        same = eq
        number = len
        non = not_
        empty = not_
        def valid(x): return non(empty(x)) and all(same(* charactes) for charactes in pairs(x))
        def score(S): return number(substring for substring in substrings(S) if valid(substring))
        # If two substrings consist of the same letters but occur at different places in S, they are still considered different.
        # For example, the score of "aaaba" is 8: there are four occurrences of the substring "a", two occurrences of "aa", one occurrence of "aaa", and one of "b".
        # On her birthday, Maki got a String s from her friend Niko as a present.
        # Calculate and return its score.
        # ROOT-0(root=Calculate-1(conj_and=return-3, dobj=score-5(poss=its-4)))
        return(score(s))



def example0():
	cls = SquareScoresDiv2()
	input0 = "aaaba"
	returns = 8
	result = cls.getscore(input0)
	return result == returns


def example1():
	cls = SquareScoresDiv2()
	input0 = "zzzxxzz"
	returns = 12
	result = cls.getscore(input0)
	return result == returns


def example2():
	cls = SquareScoresDiv2()
	input0 = "abcdefghijklmnopqrstuvwxyz"
	returns = 26
	result = cls.getscore(input0)
	return result == returns


def example3():
	cls = SquareScoresDiv2()
	input0 = "p"
	returns = 1
	result = cls.getscore(input0)
	return result == returns


def example4():
	cls = SquareScoresDiv2()
	input0 = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
	returns = 5050
	result = cls.getscore(input0)
	return result == returns



if __name__ == '__main__':
	print(example0()&example1()&example2()&example3()&example4())