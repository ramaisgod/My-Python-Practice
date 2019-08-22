# ---------- Single Inheritance -------------------

class Employee:
    no_of_leaves = 8

    def __init__(self, emp_name, emp_salary, emp_role):
        self.name = emp_name
        self.salary = emp_salary
        self.role = emp_role
        print(f"Name is {self.name}. Salary is {self.salary}. Role is {self.role}.")

joel = Employee("Joel F", 65000, "Payroll Executive")
print(joel.role)


class Professional(Employee):

    def __init__(self, emp_name, emp_salary, emp_role, emp_status):
        self.name = emp_name
        self.salary = emp_salary
        self.role = emp_role
        self.status = emp_status    

    def incometax(self):
        return f"Name is {self.name}. Salary is {self.salary}. Role is {self.role}. Status is  {self.status}"

riya = Professional("Riya Kumari", 61000, "HR Executive", "Active")
print(riya.incometax())



