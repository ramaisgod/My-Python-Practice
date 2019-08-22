# Comprehensions in Python

# **********List Comprehensions***********
# -------  Example -1 ------------  
mylist = []
for i in range(100):
    if i%3 == 0:
        mylist.append(i)

print(mylist)

# -------  Example -2 ------------  
mylist = [i for i in range(100) if i%3 == 0]
print(mylist)


# **********Dictionary Comprehensions*************
# -------  Example -1 ------------  
dict1 = {i:f"MyItem-{i}" for i in range(10) if i%2 == 0}
print(dict1)
# Reverse the item of dictionary 
dict1 = {value:key for key, value in dict1.items()}
print(dict1)

# **********Set Comprehensions*************
# -------  Example -1 ------------  
name = {name for name in ["Ram", "Shyam", "Ram", "Shyam", "Ram"] }

print(name)
print(type(name))

# **********Generator Comprehensions*************
# -------  Example -1 ------------  
# use ( ) this backet for generator
gen = (i for i in range(100) if i%2==0)
print(type(gen))
print(gen.__next__())
print(gen.__next__())

# for item in gen:
#     print(item)





