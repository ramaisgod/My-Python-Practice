# Python
# ----------- Data type ----------
# i = 20
# j = "harbu"
# k = 50.6
# print(type(k))

# -- for comment press Ctrl + /
# -------- Split ------------------
# name = "Abhishek Sarswat"
# print(name.split(" "))
# print(type(name.split(" ")))
# print(name.split(" ")[1])

# name = "Abhishek Sarswat Chauhan"
# fname = name.split(" ")[0]
# print("First Name:", fname)
# lname = name.split(" ")[-1]
# print("Last Name:", lname)
# middle_name = name.split(" ")[1]
# print("Middle Name:", middle_name)

# ----------- in and not in keyword ------------
# myString = "Ram Krishna Prasad"
#
# if "Sarswat" in myString:
#     print("Found")
# else:
#     print("Not Found")
#
#
# if "Sarswat" not in myString:
#     print("Found")
# else:
#     print("Not Found")

# --------- List ---------------------
my_list = ["rmz", "asw"]
my_list.append("vvm")  # add item at last in the list
print(my_list)
my_list.append("awj")
print(my_list)

my_list.pop()  # remove last element from list
print(my_list)

my_list.insert(2, "akn") # add item on specified position in list
print(my_list)

my_list.remove("rmz")
print(my_list)

my_list.reverse()
print(my_list)

# harbu = my_list.copy()
# print(harbu)

# del my_list
# print(harbu)

babu = my_list

print(babu)
del my_list
print("babu is ", babu)

my_list.clear()
print(my_list)










# fruits = ["45", "56", "23", "45", "43", "34", "asw", "awj", "rmz", "87", "vvm"]
# print(type(fruits))
# print(fruits.count(45))
# print(len(fruits))

# fruits.sort(reverse=True)
# for item in fruits:
#     if item.isnumeric():
#         print("Numeric : ", item)
#     else:
#         print("String : ", item)

# ------ seperate string and numeric -----------
# num = []
# myStr = []
# for item in fruits:
#     if item.isnumeric():
#         num.append(item)
#     else:
#         myStr.append(item)
#
#
# print("Numeric List are ", num)
# print("String list are ", myStr)




































