f = open("ram.txt")
# content = f.read()
# print(content)
# f.close()


# content = f.read(16)  # this will print first 7 char form file
# print(content)
# content = f.read(10)  # this will print next 7 char from file
# print(content)
# f.close()

# print("-------Print line by line--------")
# content = f.readlines() # This will read complete one line at once
# print(content)
# print([item.replace("\n", "") for item in content])


# print(type(content))
# for line in content:
#     print(line, end="")
# f.close()

print(f.readline()) # Print 1st line from file
print(f.readline()) # Print 2nd line from file
f.seek(0)
print(f.readline()) # Print 2nd line from file

