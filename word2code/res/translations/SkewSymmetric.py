from utils import *

class SkewSymmetric:
    def minChanges(self, M):
        input_array = M
        # A skew symmetric matrix M satisfies M T = - M , where M T denotes the transpose of the matrix M and - M denotes the matrix obtained by multiplying each entry of M by -1.
        def skew_symmetric(i,j): M[i,j] = -M[j,i]
        # The transpose of a matrix M is obtained by replacing the element in the i 'th row and j 'th column of M with the element in the j 'th row and i 'th column of M .
        # Note that this requires the diagonal elements of a skew-symmetric matrix to be equal to 0.
        # Create a class SkewSymmetric which contains a method minChanges.
        # The method will take a String[] M , each element of which is a single space separated list of integers.
        # The j 'th number in the i 'th element of M represents the value at row i and column j of the matrix.
        # The method should return the minimum number of values in M that must be changed such that the resulting matrix is skew symmetric.
        # ROOT-0(root=return-4(nsubj=method-2(det=The-1), aux=should-3, dobj=number-7(det=the-5, amod=minimum-6, prep_of=values-9(prep_in=M-11), rcmod=changed-15(nsubjpass=that-12, aux=must-13, auxpass=be-14, prep=such-16, ccomp=skew-22(mark=that-17, nsubj=matrix-20(det=the-18, amod=resulting-19), aux=is-21, acomp=symmetric-23)))))
        return(minimum(number(changed(values(M),skew_symmetric))))



def example0():
	cls = SkewSymmetric()
	input0 = ["1 2 8", "-2 1 0", "3 99 3"]
	returns = 5
	result = cls.minChanges(input0)
	return result == returns


def example1():
	cls = SkewSymmetric()
	input0 = ["0 1 1 1 1 1", "-1 0 1 1 1 1", "-1 -1 0 1 1 1", "-1 -1 -1 0 1 1", "-1 -1 -1 -1 0 1", "0 0 0 0 0 0"]
	returns = 5
	result = cls.minChanges(input0)
	return result == returns


def example2():
	cls = SkewSymmetric()
	input0 = ["0 0 0 0", "0 0 0 0", "0 0 0 0", "0 0 0 0"]
	returns = 0
	result = cls.minChanges(input0)
	return result == returns


def example3():
	cls = SkewSymmetric()
	input0 = ["1 0", "0 1"]
	returns = 2
	result = cls.minChanges(input0)
	return result == returns



if __name__ == '__main__':
	print(example0())