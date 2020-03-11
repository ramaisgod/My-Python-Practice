'''
The factorial of a number is the product of all the integers from 1 to that number.
For example, the factorial of 6 is 1*2*3*4*5*6 = 720.
Factorial is not defined for negative numbers, and the factorial of zero is one, 0! = 1
'''

num = 6
if num < 0:
    print("Invalid Number !!!")
elif num == 0:
    print("Factorial of 0 = 1")
factorial = 1
for i in range(1, num+1):
    factorial = factorial * i
print("Factorial of {} = {}".format(num, factorial))
