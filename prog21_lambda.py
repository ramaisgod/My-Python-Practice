# Lambda function or anonymous function 

#minus = lambda a, b: a - b
#print(minus(10,8))

# def minus(a, b):
#     return a-b

# print(minus(10,8))
def a_first(a):
    return a[1]
    # return a[0]

mylist = [[1, 14], [4, 6], [11, 2], [5, 15]]
mylist.sort(key=a_first)

print(mylist)

