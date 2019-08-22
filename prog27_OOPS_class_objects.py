'''
Concept of OOPS:
Abstraction
Encapsulation
Inheritance
Polymorphism
'''
# ---------- Example -1 ---------------------------------
# Understand class and instance
# class Student:
#     pass

# harry = Student()  # first instance of class student
# marry = Student()  # second instance of class student
# # print(harry, marry)
# harry.name = "Harry Kumar"
# harry.age = 32
# marry.name = "Marry John"
# marry.subject = ["Physics", "Chemistry", "Math"]
# print(harry.name, marry.subject)
# ---------- Example -2 ---------------------------------
class Employee:
    no_of_leaves = 12
    pass

ram = Employee()
joel = Employee()

ram.name = "Ram Krishna"
ram.salary = 40000

joel.name = "Joel F."
joel.salary = 41000

print(ram.name, joel.name)
print(ram.no_of_leaves)
print(joel.no_of_leaves)

ram.no_of_leaves = 20 # It will create a new variable for this instance. Can not change the value of class's variables by other instance.


print(ram.__dict__)
print(joel.__dict__)

print(Employee.__dict__)
Employee.no_of_leaves = 15 # Change the value of class's variables
print(Employee.__dict__)








