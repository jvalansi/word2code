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
    superior = [-1, 0] 
    workType = [1, 2]
    gcdt = GoodCompanyDivTwo()
    result = gcdt.countGood(superior, workType)
    returns = 2
    return result == returns
    
if __name__ == '__main__':
    print(example0())