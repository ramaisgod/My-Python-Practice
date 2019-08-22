# 'is' vs '==': What's The Difference?

a = [4,6,9]
b = a
print(b)
print(a==b)
print(b is a)
# a[0]=5
# print(b)


c = a[:]
print(c)
print(a==c)
print(c is a) 

