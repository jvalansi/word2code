from utils import *

class Pronunciation:
    def canPronounce(self, words):
        input_array = words
        # Peter has problems with pronouncing difficult words.
        # In particular he can't pronounce words that contain three or more consecutive consonants (such as "street" or "first").
        def cant_pronounce(word): contain(word, three or more(consecutive(consonants)))
        # Furthermore he can't pronounce words that contain two or more consecutive vowels that are different (such as "goal" or "beauty").
        # ROOT-0(root=pronounce-5(advmod=Furthermore-1, nsubj=he-2, aux=ca-3, neg=n't-4, dobj=words-6(rcmod=contain-8(nsubj=that-7, dobj=vowels-13(num=two-9(conj_or=more-11), amod=consecutive-12, rcmod=different-16(nsubj=that-14, cop=are-15, prep_such_as=goal-21(conj_or=beauty-25)))))))
        def cant_pronounce(word): dobj=words(rcmod=contain(dobj=vowels(num=two(conj_or=more), amod=consecutive, rcmod=different)))
        # He can pronounce words with two consecutive equal vowels though (such as "need").
        # Is this problem we consider the 'y' to be always a consonant, even in words like "any".
        # ROOT-0(root=problem-3(cop=Is-1, det=this-2, rcmod=consider-5(nsubj=we-4, dobj=y-8(det=the-6), xcomp=consonant-14(aux=to-10, cop=be-11, advmod=always-12, det=a-13, advmod=even-16, prep_in=words-18(prep=like-19(dep=any-21))))))
        # So the vowels are 'a', 'e', 'i', 'o' and 'u'.
        # You are given a String[] words .
        # If Peter can pronounce all the words, return an empty String; otherwise return the first word he can't pronounce.
        # ROOT-0(root=return-9(advcl=pronounce-4(mark=If-1, nsubj=Peter-2, aux=can-3, dobj=words-7(predet=all-5, det=the-6)), dobj=String-12(det=an-10, amod=empty-11), parataxis=return-15(advmod=otherwise-14, dobj=word-18(det=the-16, amod=first-17), dep=pronounce-22(nsubj=he-19, aux=ca-20, neg=n't-21))))
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