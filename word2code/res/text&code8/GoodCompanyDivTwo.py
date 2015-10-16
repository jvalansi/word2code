from problem_utils import *
from operator import *


class GoodCompanyDivTwo:
    def countGood(self, superior, workType):
        input_array1 = superior
        input_array2 = workType
        N = len(input_array1)
        
        
        
        # Shiny has a company.
        # There are N employees in her company.
        # The employees are numbered 0 through N-1 in order in which they joined the company.
        # Employee 0 is the only employee with no boss.
        # Every other employee has precisely one direct boss in the company.
        # You are given a int[] input_array1 with N elements.
        # Element 0 of input_array1 will be -1 to denote that employee 0 has no boss.
        # For each i between 1 and N-1, inclusive, element i of input_array1 will be the number of the boss of employee i.
        # For each employee, their boss joined the company before them.
        # Formally, for each i between 1 and N-1, inclusive, input_array1[i] will be between 0 and i-1, inclusive.
        # Each employee only does one type of work.
        # You are given a int[] input_array2 with N elements.
        # (Different integers represent different types of work.)
        # Each employee of the company has their own department.
        # The department of employee x is formed by employee x and all the employees such that x is their boss.
        def mapping0(possibility):
            #### def valid(possibility0): return formed(x, boss[possibility0])
            def valid(possibility0): return eq(possibility, input_array1[possibility0])
            #### def reduce(possibility0): return and([x], possibility0)
            def reduce(possibility0): return add([possibility], possibility0)
            #### return reduce(filter(valid, employees))
            return reduce(filter(valid, possibilities))
        # Formally, for any y different from x, employee y belongs into the department of employee x if and only if input_array1[y]=x.
        # Note that if input_array1[z]=y and input_array1[y]=x, employee z does not belong into the department of employee x.
        # A department is called diverse if no two employees in the department do the same type of work.
        def valid0(possibility):
            #### possibilities = two(department)
            possibilities = pairs(possibility)
            #### def mapping(possibility): return same(type_of_work[employees[0]], type_of_work[employees[1]])
            def valid(possibility): return eq(input_array2[possibility[0]], input_array2[possibility[1]])
            #### def reduce(possibility): return no(possibility)
            def reduce(possibility): return not_(possibility)
            #### return reduce(map(mapping, possibilities))
            return reduce(filter(valid, possibilities))
        # Compute and return the number of diverse departments in Shiny's company.
        #### possibilities = range(N)
        possibilities = range(N)
        #### def reduce(possibility): return number(possibility)
        def reduce(possibility): return len(possibility)
        #### return reduce(filter(valid0, map(diverse, departments)))
        return reduce(filter(valid0, map(mapping0, possibilities)))

def example0():
	cls = GoodCompanyDivTwo()
	input0 = [-1, 0]
	input1 = [1, 2]
	returns = 2
	result = cls.countGood(input0, input1)
	return result == returns

def example1():
	cls = GoodCompanyDivTwo()
	input0 = [-1, 0]
	input1 = [1, 1]
	returns = 1
	result = cls.countGood(input0, input1)
	return result == returns

def example2():
	cls = GoodCompanyDivTwo()
	input0 = [-1, 0, 1, 1]
	input1 = [1, 4, 3, 2]
	returns = 4
	result = cls.countGood(input0, input1)
	return result == returns

def example3():
	cls = GoodCompanyDivTwo()
	input0 = [-1, 0, 1, 0, 0]
	input1 = [3, 3, 5, 2, 2]
	returns = 4
	result = cls.countGood(input0, input1)
	return result == returns

def example4():
	cls = GoodCompanyDivTwo()
	input0 = [-1, 0, 1, 1, 1, 0, 2, 5]
	input1 = [1, 1, 2, 3, 4, 5, 3, 3]
	returns = 7
	result = cls.countGood(input0, input1)
	return result == returns

def example5():
	cls = GoodCompanyDivTwo()
	input0 = [-1, 0, 0, 1, 1, 3, 0, 2, 0, 5, 2, 5, 5, 6, 1, 2, 11, 12, 10, 4, 7, 16, 10, 9, 12, 18, 15, 23, 20, 7, 4]
	input1 = [4, 6, 4, 7, 7, 1, 2, 8, 1, 7, 2, 4, 2, 9, 11, 1, 10, 11, 4, 6, 11, 7, 2, 8, 9, 9, 10, 10, 9, 8, 8]
	returns = 27
	result = cls.countGood(input0, input1)
	return result == returns

if __name__ == '__main__':
    print(example0())