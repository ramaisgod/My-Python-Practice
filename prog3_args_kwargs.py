# Example of *args and **kwargs
def emp_info_function(empid, name, salary):
    print("Employee ID is ", empid, "Employee Name is ", name, "Employee Salary is ", salary)

emp_info_function(451, "ram krishna", 560000)


def emp_info_function_2(*args):
    if len(args) == 3:
        print("Employee ID is", args[0], "Employee Name is", args[1], "and Employee Salary is", args[2])
    else:
        print("Employee ID is", args[0], "Employee Name is", args[1])
            
emp_info_function_2(51, "Neetu Prasad", 60000)
emp_info_function_2(41, "Suman Vishwakarma")

list_1 = [58, "ASW", 8000]
emp_info_function_2(*list_1)


emp_list = {"Ram": 57000, "Neetu": 870000, "ASW": 67000, "Nisha": 69000, "Rohit": 89000, "Dimpu": 76000}
def print_salary(**kwargs):
    for key, value in kwargs.items():
        print(key, value)


print_salary(**emp_list)

