

class Employee:
    no_of_leaves = 8

    def __init__(self, emp_name, emp_salary, emp_role):
        self.name = emp_name
        self.salary = emp_salary
        self.role = emp_role

    @classmethod
    def from_mystr(cls, string):
        params = string.split("-")
        # return cls(*string.split("-"))
        return cls(params[0], params[1], params[2])
    
    @staticmethod
    def printmyname(string):
        print("My Name is " + string)
        

ram = Employee("Ram K. Prasad", 89000, "Lead - Reporting Automation")
asw = Employee.from_mystr("Abhishek-72000-Business Analyst")
# print(ram.salary)
print(ram.role)
print(asw.role)
Employee.printmyname("Ram")


