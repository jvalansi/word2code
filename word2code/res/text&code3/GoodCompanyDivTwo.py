from utils import *
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
        # You are given a int[] superior with N elements.
        # Element 0 of superior will be -1 to denote that employee 0 has no boss.
        # For each i between 1 and N-1, inclusive, element i of superior will be the number of the boss of employee i.
        
        # For each employee, their boss joined the company before them.
        # Formally, for each i between 1 and N-1, inclusive, superior[i] will be between 0 and i-1, inclusive.
        
        # Each employee only does one type of work.
        # You are given a int[] workType with N elements.
        # (Different integers represent different types of work.)
        
        # Each employee of the company has their own department.
        
        # The department of employee x is formed by employee x and all the employees such that x is their boss.
        #### department = lambda x: [x] and [employee for employee in employees(N) if is(boss[employee], x)]
        mapping = lambda i: [i] + [j for j in range(N) if eq(input_array1[j], i)]

        # Formally, for any y different from x, employee y belongs into the department of employee x if and only if superior[y]=x.
        # Note that if superior[z]=y and superior[y]=x, employee z does not belong into the department of employee x.
        
        # A department is called diverse if no two employees in the department do the same type of work.
        #### diverse = lambda department: no any(eq([type_of_work[employees[0]], type_of_work[employees[1]]) for employees in two(department)])  
        valid = lambda i: not any([eq(input_array2[pair[0]], input_array2[pair[1]]) for pair in pairs(i)])  

        # Compute and return the number of diverse departments in Shiny's company.
        #### return(number([diverse(possibility) for possibility in departments(N) if valid(mapping(i))]))
        return(len([mapping(possibility) for possibility in range(N) if valid(mapping(possibility))]))
    
if __name__ == '__main__':
    superior = [-1, 0] 
    workType = [1, 2]
    gcdt = GoodCompanyDivTwo()
    print(gcdt.countGood(superior, workType))
