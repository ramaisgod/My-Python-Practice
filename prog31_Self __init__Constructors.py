# -------- self and __init__ -----------------------------

# ---------------- self example ----------------------- 
class Employee:
    no_of_leaves = 8

    def printdetails(self):
        return f"Name is {self.name}. Salary is {self.salary}. and Role is {self.role}"

rohan = Employee()

rohan.name = "Rohan K"
rohan.salary = 43000
rohan.role = "Manager"
print(rohan.printdetails())

# ---------------- __init__ constructor example -----------------------
# __init__ constructor is used to pass the arguments to object.
 
class Employee2:
    def __init__(self, emp_name, emp_salary, emp_role):
        self.name = emp_name
        self.salary = emp_salary
        self.role = emp_role

ram2 = Employee2("Ram K. Prasad", 89000, "Lead - Reporting Automation")

print(ram2.salary)
print(ram2.role)
