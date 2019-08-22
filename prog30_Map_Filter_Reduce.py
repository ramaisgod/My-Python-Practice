
#---- Map Function --------------------------------------------------------
print("#---- Map Function --------------------------------------------------------")
# It apply any function to all list items. map is a kind of object

# ------- Example -1 ------------------------------
print(" ------- Example -1 ------------------------------")
# convert all list items into integer format
#-- Normal method ---
num = ["23", "32", "44", "64", "5"]  # list item is in string format
print(num)

for i in range(len(num)):
    num[i] = int(num[i])
print(num)
print(num[2]+1)  # add 1 in third element of list

#-- using Map function. ---
num = list(map(int, num))
print(num)

# ------- Example -2 ------------------------------
print("------- Example -2 ------------------------------")
# convert all list items into square using map function
# --- Method -1 -------
num = [4, 5, 9, 25, 12, 3]
num = list(map(lambda x: x*x, num))
print(num)

# --- Method -2 -------
num = [4, 5, 9, 25, 12, 3]
def sq(x):
    return x*x
num = list(map(sq, num))
print(num)

# ------- Example -3 ------------------------------
print("------- Example -3 ------------------------------")

def squ(x):
    return x*x

def cube(x):
    return x*x*x

myfunc = [squ, cube]
num = [4, 5, 9, 25, 12, 3]
for item in num:
    val = list(map(lambda x: x(item), myfunc))
    print(val)


#---- Filter Function --------------------------------------------------------
print("#---- Filter Function --------------------------------------------------------")
# It creates a list where given criteria/function returns true

list_1 = [1,2,3,4,5,6,7,8,9]

def is_greater_5(num):
    return num>5

greater_than_5 = list(filter(is_greater_5, list_1))
print(greater_than_5)

#---- Reduce Function --------------------------------------------------------
print("#---- Reduce Function --------------------------------------------------------")
# It is a part of functools. It is used to apply any function to each element of given list in sequence. 
from functools import reduce
list_2 = [1, 2, 3, 4, 5]
list_3_sum = reduce(lambda x,y: x+y, list_2)
print("Sum of list_2 is : ", list_3_sum)








