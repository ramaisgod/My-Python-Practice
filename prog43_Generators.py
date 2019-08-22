# Generators In Python 

"""
Iterable = __iter__()  or  __getitem__()
Iterator = __next__()
Iteration 

Create own generator to generate on the fly value just like "for loop". 
Generator can iterate once at a time
"""
# ---- Example -1 ------------
def my_gen(n):
    for i in range(n):
        yield i
g = my_gen(3)
print(g)
print(g.__next__())
print(g.__next__())
print(g.__next__())

# ---- Example -2 ------------
myStr = "Ram Krishna"   # integer object not iterable 
i = iter(myStr)
print(i.__next__())
print(i.__next__())
print(i.__next__())






