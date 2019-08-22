# ---- Object Introspection ---------
# it is used to know the information about object like, type, class, id, etc.


class Employee:
    def __init__(self, ename, esal):
        self.name = ename
        self.salary = esal

    def print_emp_salary(self):
        return f"Employee Name is {self.name} and Salary is {self.salary}"
    
    @property
    def email(self):
        if self.name == None:
            return "Email is not set. Please set using setter."
        return f"{self.name}@codewithharry.com"

emp1 = Employee("Ram", 7900000)
print(emp1.email)

print(type(emp1))
print(id(emp1))
a = "I am a boy"
print(id(a))
print(dir(emp1))

import inspect
print(inspect.getmembers(emp1))








