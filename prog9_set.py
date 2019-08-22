# Set theory in python 
# set store the unique value. can not append two same value in set
s = set()
#print(type(s))
# mylist = [4, 6, 9, 2, 12, 1] 
# set_from_list = set(mylist)
# print(set_from_list)
# print(type(set_from_list))

# s.add(24)
# s.add(24)
# print(s) # set store the unique value. can not append two same value in set
# s.add(24)
# s.add(25)
# print(s)
# s.add(1)
# s.add(3)
# s1 = s.union()
# print(s1)
L1 = [1, 2, 3, 4]
s1 = set(L1)
L2 = [2, 3, 4, 5, 6]
s2 = set(L2)
s = s1.union(s2)
print(s)
s = s1.intersection(s2)
print(s)
s = s1.isdisjoint(s2)
print(s)






