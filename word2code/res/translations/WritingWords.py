from problem_utils import *

class WritingWords:
    def write(self, word):
        input_array = word
        # Fox Ciel wants to type a word on her old cell phone.
        # The cell phone has only one button.
        # The letter A is typed by tapping the button once, B by tapping it twice in a row, and so on, in alphabetical order.
        tap = lambda letter: 1 if letter == 'A' else 2 if letter == 'B'... 
        # Thus, the last letter Z is typed by tapping the button 26 times without a pause.
        # You are given a String word .
        # Compute and return the answer to the following question: How many times will Ciel tap the button while typing this word?
        return(how_many(times))



def example0():
	cls = WritingWords()
	input0 = "A"
	returns = 1
	result = cls.write(input0)
	return result == returns


def example1():
	cls = WritingWords()
	input0 = "ABC"
	returns = 6
	result = cls.write(input0)
	return result == returns


def example2():
	cls = WritingWords()
	input0 = "VAMOSGIMNASIA"
	returns = 143
	result = cls.write(input0)
	return result == returns


def example3():
	cls = WritingWords()
	input0 = "TOPCODER"
	returns = 96
	result = cls.write(input0)
	return result == returns


def example4():
	cls = WritingWords()
	input0 = "SINGLEROUNDMATCH"
	returns = 183
	result = cls.write(input0)
	return result == returns


def example5():
	cls = WritingWords()
	input0 = "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"
	returns = 1300
	result = cls.write(input0)
	return result == returns



if __name__ == '__main__':
	print(example0())