from problem_utils import *
from string import punctuation, digits, whitespace
from re import split, escape

class TextStatistics:
    def averageLength(self, text):
        input_array = text
        # Most modern text editors are able to give some statistics about the text they are editing.
        # One nice statistic is the average word length in the text.
        # A word is a maximal continuous sequence of letters ('a'-'z', 'A'-'Z').
        # Words can be separated by spaces, digits, and punctuation marks.
        separated = split
        spaces = whitespace
        words = separated('['+escape(spaces+digits+punctuation)+']', text)
        # The average word length is the sum of all the words' lengths divided by the total number of words.
        # For example, in the text "This is div2 easy problem.
        # ", there are 5 words: "This", "is", "div", "easy", and "problem".
        # The sum of the word lengths is 4+2+3+4+7=20, so the average word length is 20/5=4.
        # Given a String text , return the average word length in it.
        length = len
        return(average(list(length(word) for word in words if word)))
        # If there are no words in the text, return 0.0.



def example0():
	cls = TextStatistics()
	input0 = "This is div2 easy problem."
	returns = 4.0
	result = cls.averageLength(input0)
	return result == returns


def example1():
	cls = TextStatistics()
	input0 = "Hello, world!"
	returns = 5.0
	result = cls.averageLength(input0)
	return result == returns


def example2():
	cls = TextStatistics()
	input0 = "Simple"
	returns = 6.0
	result = cls.averageLength(input0)
	return result == returns


def example3():
	cls = TextStatistics()
	input0 = ""
	returns = 0.0
	result = cls.averageLength(input0)
	return result == returns


def example4():
	cls = TextStatistics()
	input0 = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
	returns = 50.0
	result = cls.averageLength(input0)
	return result == returns



if __name__ == '__main__':
	print(example0()&example1()&example2()&example3()&example4())