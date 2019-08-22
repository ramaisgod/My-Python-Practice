# The purpose of zip() is to map the similar index of multiple containers
# so that they can be used just using as single entity.

name = ["Manjeet", "Nikhil", "Shambhavi", "Astha"]
roll_no = [4, 1, 3, 2]
marks = [40, 50, 60, 70]

myzip = zip(name, roll_no, marks)  # using zip() to map values

# for i in myzip:
#     print(i)
#     # print(type(i))


# a = set(myzip)  # converting values to print as set
# print(a)
# print(type(a))

# Unzipping means converting the zipped values back to the individual self as they were.
# This is done with the help of “*” operator.

i, j, k = zip(*myzip)
print(i)
print(j)
print(k)





