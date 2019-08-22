# *args and **kwards keywords. it is a way to pass the agruments
# args and kwargs pass the arguments as a tuple
"""
how to pass args , kwargs and one normal arguments together:
Pass first normal argements then *args then **kwargs, for example:
def myfunction(id, *args, **kwargs):
    pass
"""

def myfunc(a,b,c,d):
    print(a,b,c,d)

myfunc("rmz", "asw", "vvm", "awj")

# ----- *args Example-1-----------
print("----*args Example-1----:")
def myfunc1(*args):
    print(type(args))
    print(*args)
    
mylist = ["rmz", "asw", "vvm", "awj", "bav"]
myfunc1(*mylist)

# ----- *args Example-2-----------
print("----*args Example-2----:")
def myfunc2(*args):
    for item in args:
        print(item)

myfunc2(*mylist)

# ----- *args Example-3-----------
print("----*args Example-3----:")
def myfunc3(a, *args):
    print(a)
    for item in args:
        print(item)

a = "This is employee code."
myfunc3(a, *mylist)



