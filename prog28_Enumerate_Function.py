# Example of Enumerate Function 

mylist = ["RMZ", "ASW", "AWJ", "VVM", "SII", "NIS", "SWO", "GTY"]

# I want to print list item which is on odd position like 1, 3, 5 ...

# Normal method :
print("Normal method")
i=1
for item in mylist:
    if i%2 is not 0:  # it will return only odd
        print(item)
    i += 1

# using Enumerate function this function return index and item both. index start from 0 :
print("using Enumerate function")
for index, item in enumerate(mylist):
    if index %2 == 0:
        print(item)



