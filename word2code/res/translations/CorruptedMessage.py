from utils import *
from string import lowercase

class CorruptedMessage:
	def reconstructMessage(self, s, k):
		input_array = s
		input_int = k
		N = len(input_array)
		possibilities = lowercase
		'''  Your friend just sent you a message.'''
		# The message consisted of one or more copies of the same lowercase letter.
		copies = mul
		mapping = lambda possibility: copies(possibility,N)
		# For example, "aaaaa" and "xxxxxxxxx" are valid messages.
		# Unfortunately, on its way to you the message became corrupted: exactly k letters of the original message were changed to some other letters.
		message = s
		changed = diff
		exactly = eq
		valid = lambda possibility: exactly(k, len(changed(message,possibility)))
		# The message you received is s .
		# Given the String s and the int k , reconstruct the original message.
		# More precisely, return a String that could have been the original message.
		could = valid
		return(filter(valid, (map(mapping, possibilities)))[0])
		# It is guaranteed that at least one such String will always exist.
		# If there are multiple possible answers, you may return any of them. 

def example0():
	cls = CorruptedMessage()
	input0 = "hello"
	input1 = 3
	returns = "lllll"
	result = cls.reconstructMessage(input0, input1)
	return result == returns

def example1():
	cls = CorruptedMessage()
	input0 = "abc"
	input1 = 3
	returns = "ddd"
	result = cls.reconstructMessage(input0, input1)
	return result == returns

def example2():
	cls = CorruptedMessage()
	input0 = "wwwwwwwwwwwwwwwwww"
	input1 = 0
	returns = "wwwwwwwwwwwwwwwwww"
	result = cls.reconstructMessage(input0, input1)
	return result == returns

def example3():
	cls = CorruptedMessage()
	input0 = "ababba"
	input1 = 3
	returns = "aaaaaa"
	result = cls.reconstructMessage(input0, input1)
	return result == returns

def example4():
	cls = CorruptedMessage()
	input0 = "zoztxtoxytyt"
	input1 = 10
	returns = "oooooooooooo"
	result = cls.reconstructMessage(input0, input1)
	return result == returns

def example5():
	cls = CorruptedMessage()
	input0 = "jlmnmiunaxzywed"
	input1 = 13
	returns = "mmmmmmmmmmmmmmm"
	result = cls.reconstructMessage(input0, input1)
	return result == returns

if __name__ == '__main__':
	print(example0())

