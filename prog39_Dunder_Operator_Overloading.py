# --- Operator Overloading & Dunder Methods  -------
# https://docs.python.org/3/library/operator.html
# Mapping Operators to Functions

class Employee:
    def __init__(self, ename, esalary, erole):
        self.name = ename
        self.salary = esalary
        self.role = erole
    
    def emp_info(self):
        return f"Name is {self.name}. Salary is Rs. {self.salary}. Role is {self.role}."
    
    # below is dunder method to add two objects, operator overloading
    def __add__(self, other):
        return self.salary + other.salary
    
    def __truediv__(self, other):
        return self.salary / other.salary
    
    def __repr__(self):
        # return self.emp_info()
        return f"Employee('{self.name}', {self.salary}, '{self.role}')" 

    def __str__(self):
        return self.emp_info()

emp1 = Employee("ASW", 32000, "Business Analyst")
# emp2 = Employee("VVM", 22000, "MIS Executive")
# print(emp1 + emp2)
# print(emp1 / emp2)
print(emp1)
# -------- __str__ will run first if both __repr__ and __str__ are present -----------
print(repr(emp1))
print(str(emp1))

