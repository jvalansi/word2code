from utils import *

class SlimeXSlimeRancher2:
    def train(self, attributes):
        input_array = attributes
        # You are playing a game titled Slime Rancher 2.
        # You will be training slimes in this game.
        # You have a slime-in-training.
        # Associated with the slime are N attributes, numbered 0 through N-1, each represented by a positive integer.
        # You are given int[] attributes containing N integers : the i-th integer is the initial value of the i-th attribute for the slime.
        # After the training is complete, each of the slime's attributes will either stay the same or increase to some positive integer less than or equal to 999.
        # None of the attributes will decrease in value.
        # The weight of the training is defined as the sum of the differences between the final and initial values of all the attributes for the slime.
        # ROOT-0(root=defined-7(nsubjpass=weight-2(det=The-1, prep_of=training-5(det=the-4)), auxpass=is-6, prep_as=sum-10(det=the-9, prep_of=differences-13(det=the-12, prep_between=values-19(det=the-15, amod=final-16(conj_and=initial-18), prep_of=attributes-23(predet=all-21, det=the-22, prep_for=slime-26(det=the-25)))))))
        def weight(training): sum(differences(final,initial))
        # You are a master slime breeder, and you're able to obtain any possible final values for a slime's attributes.
        # This time, you would like to create a well-balanced slime.
        # A slime is well-balanced if all of its attributes have equal values.
        def well_balanced(slime): all(attributes,equal(value))
        # What is the minimum possible weight of the training?
        # ROOT-0(root=What-1(cop=is-2, nsubj=weight-6(det=the-3, amod=minimum-4, amod=possible-5, prep_of=training-9(det=the-8))))
        minimum(possible(weight(training)))



def example0():
	cls = SlimeXSlimeRancher2()
	input0 = [1,2,3]
	returns = 3
	result = cls.train(input0)
	return result == returns


def example1():
	cls = SlimeXSlimeRancher2()
	input0 = [5,5]
	returns = 0
	result = cls.train(input0)
	return result == returns


def example2():
	cls = SlimeXSlimeRancher2()
	input0 = [900,500,100]
	returns = 1200
	result = cls.train(input0)
	return result == returns



if __name__ == '__main__':
	print(example0())