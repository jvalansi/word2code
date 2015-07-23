from utils import *

class Pronunciation:
    def canPronounce(self, words):
        input_array = words
        # Peter has problems with pronouncing difficult words.
        # In particular he can't pronounce words that contain three or more consecutive consonants (such as "street" or "first").
        def cant_pronounce(word): contain(word, three or more(consecutive(consonants)))
        # Furthermore he can't pronounce words that contain two or more consecutive vowels that are different (such as "goal" or "beauty").
        def cant_pronounce(word): dobj=words(rcmod=contain(dobj=vowels(num=two(conj_or=more), amod=consecutive, rcmod=different)))
        # He can pronounce words with two consecutive equal vowels though (such as "need").
        # Is this problem we consider the 'y' to be always a consonant, even in words like "any".
        # So the vowels are 'a', 'e', 'i', 'o' and 'u'.
        # You are given a String[] words .
        # If Peter can pronounce all the words, return an empty String; otherwise return the first word he can't pronounce.
#         return(dobj=word(amod=first), dep=pronounce(aux=ca, neg=n't))))
        return first(cant_pronounce(word))



def example0():
	cls = Pronunciation()
	input0 = ["All","of","these","are","not","difficult"]
	returns = ""
	result = cls.canPronounce(input0)
	return result == returns


def example1():
	cls = Pronunciation()
	input0 = ["The","word","REALLY","is","really","hard"]
	returns = "REALLY"
	result = cls.canPronounce(input0)
	return result == returns


def example2():
	cls = Pronunciation()
	input0 = ["TRiCKy"]
	returns = "TRiCKy"
	result = cls.canPronounce(input0)
	return result == returns


def example3():
	cls = Pronunciation()
	input0 = ["irresistable","prerogative","uttermost","importance"]
	returns = ""
	result = cls.canPronounce(input0)
	return result == returns


def example4():
	cls = Pronunciation()
	input0 = ["Aa"]
	returns = ""
	result = cls.canPronounce(input0)
	return result == returns



if __name__ == '__main__':
	print(example0())