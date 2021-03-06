from problem_utils import *


class TournamentsAmbiguityNumber:
    def scrutinizeTable(self, table):
        input_array = table
        N = len(table)
        
        
        
        # In a chess tournament, each pair of distinct players played a single match against each other.
        # Each match resulted in one of three outcomes: the first player won, the second player won, or there was a draw.
        # The ambiguity number of the tournament is defined as the number of distinct triples of players (a, b, c) such that player a defeated b, player b defeated player c, and player c defeated player a.
        def reduce0(possibility):
            #### def reduce(possibility): return number(possibility)
            def reduce(possibility): return sum(possibility)
            #### def mapping((a, b, c)): return (defeated((a, b)) and defeated((b, c)) and defeated((c, a)))
            def mapping((a, b, c)): return (valid0((a, b)) and valid0((b, c)) and valid0((c, a)))
            #### possibilities = triples(players)
            possibilities = triples(possibility)
            #### return(reduce(map(mapping, possibilities)))
            return reduce(map(mapping, possibilities))
        # You are given the results of all the matches as a String[] input_array .
        # The j-th character of the i-th element of input_array is '1' (one) if player i defeated player j, '0' (zero) if player j defeated player i, or '-' if the match between players i and j resulted in a draw.
        def valid0(possibility):
            #### possibilities = possibility
            possibilities = possibility
            #### reduce = lambda possibility: (table[possibility[i]][possibility[j]] == '1')
            reduce = (lambda possibility: (table[possibility[0]][possibility[1]] == '1'))
            #### return(reduce(possibilities))
            return reduce(possibilities)
        # Return the ambiguity number of the given tournament.
        #### possibilities = range(N)
        possibilities = range(N)
        #### return ambiguity_number(possibilities)
        return reduce0(possibilities)

def example0():
	cls = TournamentsAmbiguityNumber()
	input0 = ["-10", "0-1", "10-"]
	returns = 3
	result = cls.scrutinizeTable(input0)
	return result == returns


def example1():
	cls = TournamentsAmbiguityNumber()
	input0 = ["----", "----", "----", "----"]
	returns = 0
	result = cls.scrutinizeTable(input0)
	return result == returns


def example2():
	cls = TournamentsAmbiguityNumber()
	input0 = ["-1", "0-"]
	returns = 0
	result = cls.scrutinizeTable(input0)
	return result == returns


def example3():
	cls = TournamentsAmbiguityNumber()
	input0 = ["--1-10-1---1--1-00", "--0110000--0---10-", "01--00000100-00011", "-0---0010-11110100", "001--01-00-0001-1-", "11111--100--1-1-01", "-1110--00110-11-01", "0110-01--100110-10", "-111111---01--0-01", "--0-1100----10011-", "--10--011--1--101-", "01101-110-0--1-0-1", "---010-0-0---00-11", "--101-00-1-01-0-0-", "0-110001110-11-110", "-010-----011--0--0", "11010110100-010--0", "1-01-0010--00-111-"]
	returns = 198
	result = cls.scrutinizeTable(input0)
	return result == returns



if __name__ == '__main__':
	print(example0()&example1()&example2()&example3())