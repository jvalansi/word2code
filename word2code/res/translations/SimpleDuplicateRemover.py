from problem_utils import *

class SimpleDuplicateRemover:
    def process(self, sequence):
        input_array = sequence
        # We have a sequence of integers.
        # We want to remove duplicate elements from it.
        # You will be given a int[] sequence .
        # For each element that occurs more than once leave only its rightmost occurrence.
        # ROOT-0(root=leave-9(dep=For-1, nsubj=element-3(det=each-2, rcmod=occurs-5(nsubj=that-4, dobj=than-7(quantmod=more-6, quantmod=once-8))), dobj=occurrence-13(advmod=only-10, poss=its-11, amod=rightmost-12)))
        return leave(element, rightmost)
        # All unique elements must be copied without changes.



def example0():
	cls = SimpleDuplicateRemover()
	input0 = [1,5,5,1,6,1]
	returns = [5, 6, 1 ]
	result = cls.process(input0)
	return result == returns


def example1():
	cls = SimpleDuplicateRemover()
	input0 = [2,4,2,4,4]
	returns = [2, 4 ]
	result = cls.process(input0)
	return result == returns


def example2():
	cls = SimpleDuplicateRemover()
	input0 = [6,6,6,6,6,6]
	returns = [6 ]
	result = cls.process(input0)
	return result == returns


def example3():
	cls = SimpleDuplicateRemover()
	input0 = [1,2,3,4,2,2,3]
	returns = [1, 4, 2, 3 ]
	result = cls.process(input0)
	return result == returns


def example4():
	cls = SimpleDuplicateRemover()
	input0 = [100,100,100,99,99,99,100,100,100]
	returns = [99, 100 ]
	result = cls.process(input0)
	return result == returns



if __name__ == '__main__':
	print(example0())