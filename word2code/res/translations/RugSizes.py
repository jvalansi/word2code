from problem_utils import *

class RugSizes:
    def rugCount(self, area):
        input_int = area
        ways = list(combinations_with_replacement(range(inclusive(area)), 2))
        # Rugs come in various sizes.
        # In fact, we can find a rug with any integer width and length, except that no rugs have a distinct width and length that are both even integers.
        both = all
        distinct = ne
        no = not_
        even = is_even
        def valid(rug): return no(distinct(*rug) and both(even(integer) for integer in rug))
        # For example, we can find a 4x4 rug, but not a 2x4 rug.
        # We want to know how many different choices we have for a given area.
        # Create a class RugSizes the contains a method rugCount that is given the desired area and returns the number of different ways in which we can choose a rug size that will cover that exact area.
        # ROOT-0(root=Create-1(ccomp=RugSizes-4(nsubj=class-3(det=a-2), ccomp=contains-6(nsubj=the-5, dobj=rugCount-9(det=a-7, nn=method-8, rcmod=given-12(nsubjpass=that-10, auxpass=is-11, dobj=area-15(det=the-13, amod=desired-14))), conj_and=returns-17(dobj=number-19(det=the-18, prep_of=ways-22(amod=different-21), rcmod=choose-27(prep_in=which-24, nsubj=we-25, aux=can-26, dobj=size-30(det=a-28, nn=rug-29, rcmod=cover-33(nsubj=that-31, aux=will-32, dep=area-36(mark=that-34, amod=exact-35))))))))))
        number = len
        different = set
        def can(ways): return filter(valid, ways)
        def exact(ways,area): return(way for way in ways if eq(mul(*way),area))
        return(number(different(can(exact(ways,area)))))
        # Do not count the same size twice -- a 6 x 9 rug and a 9 x 6 rug should be counted as one choice.



def example0():
	cls = RugSizes()
	input0 = 4
	returns = 2
	result = cls.rugCount(input0)
	return result == returns


def example1():
	cls = RugSizes()
	input0 = 8
	returns = 1
	result = cls.rugCount(input0)
	return result == returns



if __name__ == '__main__':
	print(example0()&example1())