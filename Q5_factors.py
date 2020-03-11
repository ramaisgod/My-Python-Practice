# Python Program to find the factors of a number

num = 10
print("Factors of number {} are:".format(num))
for i in range(1, num+1):
    if num % i == 0:
        print(i, end=", ")
