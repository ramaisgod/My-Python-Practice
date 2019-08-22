# --- Multiple Inheritance -----------------------


class Employee:
    no_of_leaves = 8
    #var = 9
    def __init__(self, ename, esal, erole):
        self.name = ename
        self.salary = esal
        self.role = erole

    def print_emp_details(self):
        return f"Name is {self.name}. Salary is {self.salary}. Role is {self.role}" 
    
    @classmethod
    def from_mystring(cls, mystring):
        return cls(*mystring.split("-"))

class Player:
    var = 10
    def __init__(self, name, game):
        self.name = name
        self.game = game

    def print_player_details(self):
         return f"Name is {self.name}. Game is {self.game}." 

# inherit Employee and Player class. Note: sequence is important
# class CoolProgrammer(Employee, Player) 
class CoolProgrammer(Employee, Player):  # sequence is changed 
    language = "C++"
    #var = 11
    def print_language(self):
        print(self.language)

rmz = Employee("Ram Krishna", 7400000, "Backend Developer")
#print(rmz.print_emp_details())
#asw = Employee.from_mystring("Abhishek Sarswat-45000-Backend Developer")
#print(asw.print_emp_details())
#vvm = Player("Vivek Kumar", ["Cricket"])
nisha = CoolProgrammer("Nisha", 34000, "Executive-Programer") 
#nish = CoolProgrammer("Nisha", ["Cricket"])
#nis = nish.print_emp_details()
# nisha.print_language()
#print(nish.print_player_details())
#print(nish.var)
print(nisha.print_emp_details())
print(nisha.salary*rmz.salary)
