# --------- Query -1 -----------------------------------------------
# class myarea:
#     pi = 3.14
#     def __init__(self,length,breath,diameter):
#         self.length=length
#         self.breath=breath
#         self.diameter=diameter

#     def mytriangle(self):
#             val = (self.breath)*(self.length)*(.5)
#             return val

#     def mysquare(self):
#             return (self.length)*(self.length)

#     def mycircle(self):
#             return (myarea.pi)*(self.diameter)*2

# class volume(myarea):
#     def __init__(self,length,breath,diameter,height):
#         myarea.__init__(self,length,breath,diameter)
#         self.height=height

#     def V_triangle(self):
#             vol=myarea.mycircle(self)*self.height
#             return vol

# obj_area = myarea(3, 4, 5)
# obj_volume = volume(3, 4, 5, 6)

# #a = obj.V_triangle()
# print(obj_volume.V_triangle())

# --------- Query -2 -----------------------------------------------
# x = 1
# while x<=10:
#     print(x)
#     x += 1

# --------- Query -3 -----------------------------------------------

# def myfunc(a,b):
#     mysum = a + b
#     mymul = a * b
#     return mysum, mymul

# q = myfunc(2,3)
# print("Sum is ",q[0])
# print("Multiply is ", q[1])

# --------- Query -4 -----------------------------------------------
# word = "aeioubcdfg"
# print(word [:3] + word [3:])
# --------- Query -5 -----------------------------------------------
# list1 = ['a','e','i','o','u']
# print(list1[8:])
# --------- Query -6 -----------------------------------------------
def foo(i= []):
    i.append(1)
    return i

a = foo()
print(a)



