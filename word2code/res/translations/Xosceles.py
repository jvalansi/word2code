from problem_utils import *

class Xosceles:
    def draw(self, xCount):
        input_int = xCount
        # Little Johnny loves triangles and loves ascii art, but above of all things, loves the character 'X'.
        # His drive to mix these passions together has lead him to invent the Xosceles - Isosceles triangles made completely of 'X' characters.
        # To draw a Xosceles, Little Johnny opens a text editor begins by typing "X" or "XX" (quotes for clarity) in the middle of the first line of the text document, he follows by typing 3 or 4 'X' characters in the following line, in such a way that the second line contains 2 more 'X' characters than the first one.
        # He continues this process until he gets tired, making sure to align each line to the center (so that it forms an isoceles triangle).
        # Some example results of this process follow: (For convenience, '.'
        # characters are used instead of whitespace): ....X.... ...XXX... ..XXXXX.. .XXXXXXX.
        # XXXXXXXXX ...XX... ..XXXX.. .XXXXXX.
        # XXXXXXXX .X.
        # XXX Little Johnny has challenged you to draw a Xosceles using exactly xCount 'X' characters.
        # Return a String[] that contains xCount characters and follows the rules stated above.
        # The first element of your return value would represent the first line.
        # All lines in the return must have the same length.
        # Use '.'
        # to represent whitespace, and make sure that your return value contains as little whitespace as possible.
        # In case it is not possible to draw one of such triangles using xCount 'X' characters, return an empty String[].



def example0():
	cls = Xosceles()
	input0 = 4
	returns = [".X.", "XXX" ]
	result = cls.draw(input0)
	return result == returns


def example1():
	cls = Xosceles()
	input0 = 6
	returns = [".XX.", "XXXX" ]
	result = cls.draw(input0)
	return result == returns


def example2():
	cls = Xosceles()
	input0 = 16
	returns = ["...X...", "..XXX..", ".XXXXX.", "XXXXXXX" ]
	result = cls.draw(input0)
	return result == returns


def example3():
	cls = Xosceles()
	input0 = 18
	returns = [ ]
	result = cls.draw(input0)
	return result == returns


def example4():
	cls = Xosceles()
	input0 = 100
	returns =  [".........X.........", "........XXX........", ".......XXXXX.......", "......XXXXXXX......", ".....XXXXXXXXX.....", "....XXXXXXXXXXX....", "...XXXXXXXXXXXXX...", "..XXXXXXXXXXXXXXX..", ".XXXXXXXXXXXXXXXXX.", "XXXXXXXXXXXXXXXXXXX" ]
	result = cls.draw(input0)
	return result == returns



if __name__ == '__main__':
	print(example0())