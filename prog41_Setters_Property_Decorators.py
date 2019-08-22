# --- Setters & Property Decorators  ------------------

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
    
    @email.setter   # set new email and create name from email
    def email(self, new_email):
        print("Setting name from given email address...")
        self.name = new_email.split("@")[0] # split name from email string and set the new name
    
    @email.deleter  # delete email
    def email(self):
        self.name = None
    

emp1 = Employee("Abhishek", 24000)
emp2 = Employee("Ram", 34500)
print(emp1.print_emp_salary())
print(emp1.email)
emp1.name = "Anju"  # changing name
print(emp1.email)   # print email of new name
# set email attribute :
emp1.email = "deepak@codewithharry.com"
print(emp1.name)
print(emp1.email)

del emp1.email
print(emp1.email)

emp1.email = "sonam@gmail.com"
print(emp1.name)
print(emp1.email)


