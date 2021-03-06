from problem_utils import *


class SupermarketDiscount:
    def minAmount(self, goods):
        input_array = goods
        
        # Three girls are shopping at a supermarket.
        # The supermarket is having a sale: "Spend $50 or more in a single transaction and get $10 off."
        def spend(x):
            #### return (off(x, 10) if more(x, 50) else x)
            return (sub(x, 10) if ge(x, 50) else x)
        # The girls realize that if they combine their purchases, they might be able to pay less than if they each pay separately.
        #### possibilities = partitions(goods)
        possibilities = partitions(goods)
        # For example, if they are buying a total of $46, $62 and $9 worth of goods, respectively, they can combine the $46 and $9 totals and make two purchase transactions ($55 and $62) to get $20 off.
        # You will be given a int[] goods , each element of which is the total cost of the goods purchased by one of the girls.
        # Return the minimal total cost required to purchase all the goods.
        # 
        # The girls are willing to combine their purchases as described above, but no girl is willing to split up her goods across multiple transactions.

def example0():
	cls = SupermarketDiscount()
	input0 = [46, 62, 9]
	returns = 97
	result = cls.minAmount(input0)
	return result == returns


def example1():
	cls = SupermarketDiscount()
	input0 = [50, 62, 93]
	returns = 175
	result = cls.minAmount(input0)
	return result == returns


def example2():
	cls = SupermarketDiscount()
	input0 = [5, 31, 15]
	returns = 41
	result = cls.minAmount(input0)
	return result == returns


def example3():
	cls = SupermarketDiscount()
	input0 = [5, 3, 15]
	returns = 23
	result = cls.minAmount(input0)
	return result == returns



if __name__ == '__main__':
	print(example0()&example1()&example2()&example3())