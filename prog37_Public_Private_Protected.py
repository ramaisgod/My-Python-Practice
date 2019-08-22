
# ---- Public, Private & Protected Access Specifiers --------

class Employee:
    var1 = 9 # public variable
    _var2 = 10 # private variable - put _ before variable name
    __var3 = 11 # protected variable - put __ before variable name

    def __init__(self, ename, esal, erole):
        self.name = ename
        self.salary = esal
        self.role = erole

    def print_emp_details(self):
        return f"Name is {self.name}. Salary is {self.salary}. Role is {self.role}" 

emp = Employee("Jenilyn Aboy", "$540", "Sales")
print(emp.print_emp_details())

print("Public variable ", emp.var1)
print("Private variable", emp._var2)
print("Protected variable", emp._Employee__var3)

