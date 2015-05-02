# John couldn't handle long strings so he came up with the idea of MicroStrings.
# You are given two positive ints: A and D. 
# These determine an infinite decreasing arithmetic progression: A, A-D, A-2D, and so on. 
# Clearly, only finitely many elements of such a progression are non-negative.
# Each such progression defines one MicroString, as follows: 
# 	You take all the non-negative elements, 
# 	convert each of them into a string, 
# 	and then concatenate those strings (in order).
# For example, let A=12 and D=5. 
# For these values we get the arithmetic progression (12, 7, 2, -3, -8, ...). 
# The non-negative elements are 12, 7, and 2. 
# The corresponding strings are "12", "7", and "2". 
# Their concatenation is the following MicroString: "1272".
# Given A and D, return the MicroString they define.