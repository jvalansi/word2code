from utils import *

class RectangleGroups:
    def maximalIndexed(self, rectangles):
        input_array = rectangles
        # You have a list of rectangles divided into groups.
        # The index of a group is the sum of the areas of all the rectangles in the group.
        # ROOT-0(root=sum-8(nsubj=index-2(det=The-1, prep_of=group-5(det=a-4)), cop=is-6, det=the-7, prep_of=areas-11(det=the-10, prep_of=rectangles-15(predet=all-13, det=the-14, prep_in=group-18(det=the-17)))))
#         root=sum(nsubj=index(prep_of=group), cop=is, prep_of=areas(prep_of=rectangles(predet=all, prep_in=group))))
        def index(group): sum(areas(rectangles(group)))
        # You are to determine the group with the biggest index.
        # You are given a String[] rectangles .
        # Each element of rectangles represents a single rectangle, and is formatted as "G L W", where G is the name of the group to which the rectangle belongs, L is the rectangle's length, and W is the rectangle's width.
        def rectange(s): return re.match(r'(?P<name>\w) (?P<length>\w) (?P<width>\w)', s).groups()   
        # Return a String formatted as "G I", where G is the name of the group with the maximal index, and I is the index of that group with no leading zeroes.
        return "{G} {I}".where(G=name(max(index(group))), I=index(name(max(index(group)))))
        # If there are multiple groups with the same maximal index, return the one whose name comes first alphabetically.



def example0():
	cls = RectangleGroups()
	input0 = ["A 1 2", "A 3 3"]
	returns = "A 11"
	result = cls.maximalIndexed(input0)
	return result == returns


def example1():
	cls = RectangleGroups()
	input0 = ["A 1 2", "B 3 3", "A 2 1"]
	returns = "B 9"
	result = cls.maximalIndexed(input0)
	return result == returns


def example2():
	cls = RectangleGroups()
	input0 = ["D 1 6", "F 2 3", "G 1 1", "G 5 1", "C 3 2"]
	returns = "C 6"
	result = cls.maximalIndexed(input0)
	return result == returns


def example3():
	cls = RectangleGroups()
	input0 = ["S 2 54", "Y 34 65", "F 234 23", "D 84 127", "R 603 46", "S 36 192", "Y 76 32", "T 54 28", "S 22 22"]
	returns = "R 27738"
	result = cls.maximalIndexed(input0)
	return result == returns



if __name__ == '__main__':
	print(example0())