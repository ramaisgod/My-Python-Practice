
# -------- classmethod  -----------------------------
# classmethod is used to access only class varibales not instance variable. It takes only class input and arguments
# do not take self input

class Employee:
    no_of_leaves = 8

    def __init__(self, emp_name, emp_salary, emp_role):
        self.name = emp_name
        self.salary = emp_salary
        self.role = emp_role

    @classmethod
    def change_leaves(cls, new_leaves):
        cls.no_of_leaves = new_leaves
    
    @classmethod
    def from_mystr(cls, string):
        params = string.split("-")
        # return cls(*string.split("-"))
        return cls(params[0], params[1], params[2])
        

ram = Employee("Ram K. Prasad", 89000, "Lead - Reporting Automation")
asw = Employee.from_mystr("Abhishek-72000-Business Analyst")
# print(ram.salary)
print(ram.role)
print(asw.role)

print(Employee.no_of_leaves)
ram.no_of_leaves = 34  # you can not change the class variable via instance 
ram.change_leaves(34)
Employee.change_leaves(35)
print(Employee.no_of_leaves)
