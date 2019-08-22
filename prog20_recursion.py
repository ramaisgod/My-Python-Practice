"""
Factorial of n:
n! = n * (n-1) * (n-2) * (n-3) ........... 1
OR
n! = n * (n-1)!

"""
# def factorial_iteration(n):
#     fac = 1
#     for i in range(n):
#         fac = fac * (i+1)
#     return fac


# def factorial_recursive(n):
#     if n == 1 or n == 0:
#         return 1
#     else:
#         return n * factorial_recursive(n-1)
    

# num = int(input("Enter Number to Find Factorial: "))
# print(factorial_iteration(num))
# print(factorial_recursive(num))

# ------- fibonacci numbers --- 0 1 1 2 3 5 8 13 --------
def fibonacci_number(n):
    if n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        return fibonacci_number(n-1) + fibonacci_number(n-2)

num = int(input("Enter Number : "))
print(fibonacci_number(num))
