'''
------- Example -1 -----------------
'''
# def myfunc1():
#     print("Hello, I am Ram")

# myfunc2 = myfunc1
# del myfunc1
# myfunc2()

'''
 ------- Example -2 -----------------
You can return a Function using a function. Function can return function.
'''
# def myfunction_1(num):
#     if num == 0:
#         return print
#     if num == 1:
#         return sum

# a = myfunction_1(0)
# print(a)
# a = myfunction_1(1)
# print(a)

'''
 ------- Example -3 -----------------
Pass function as an argument of a function
'''
# def myfunction_2(myfunction_1):
#     myfunction_1("Hello Python Decorators")

# myfunction_2(print)

'''
 ------- Example -4 -----------------
Decorator
'''
def dec1(func1):
    def nowexec():
        print("Execute Now")
        func1()
        print("Executed")
    return nowexec

@dec1 
def Ram_function():
    print("Ram is a good boy")

#Ram_function = dec1(Ram_function)
Ram_function()












