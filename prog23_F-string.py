# F-string 

name = "Ram Krishna"
age = "30"

# Method - 1 -------------
# mystring = "My name is %s and my age is %s" %(name,age)
# print(mystring)

# Method - 2 -------------
# mystring = "My name is {} and my age is {}"
# mystring = "My name is {1} and my age is {0}"
# mystr = mystring.format(name, age)
# print(mystr)

# f string Example -1 -------------
mystring = f"My name is {name} and my age is {age}. sum of 4 and 5 is {4+5}"
print(mystring)

# f string Example -2 -------------
import math
mystring = f"My name is {name} and my age is {age}. value of cos65 is {math.cos(65)}"
print(mystring)




