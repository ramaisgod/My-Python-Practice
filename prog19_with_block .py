with open("ram.txt") as f:
    a = f.readlines()
    print(a)

fl = open("ram.txt", "rt")
print(fl.readline())
fl.close()