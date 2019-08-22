f = open("ram2.txt")
print(f.tell()) # it returns the current positon of file pointer f.
print(f.readline())
print(f.tell())
f.seek(0) # Change the current position of file pointer f.
print(f.readline())
print(f.tell())
f.close()
