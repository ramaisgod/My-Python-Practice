# Open file in write mode
# f = open("ram2.txt", "w") 
# f.write("I am 30 years old.")
# f.close()
# """
# This will open ram2.txt file and replace all the contents.
# But If file does not exists then it will create new file and replace all the contents.
# """

# Open file in append mode
# f = open("ram3.txt", "a")
# f.write("My DOB is 2-Jan-1987.\n")
# f.close()
# """
# This will open ram2.txt file and add the contents at end of the file.
# But If file does not exists then it will create new file add the contents at end of the file.
# """

# Add contents in file and print no of charector
# f = open("ram2.txt", "a")
# i = f.write("Ram is a good boy.\n")
# print(i) # This will print total no of char of i
# f.close()

# Handle read and write mode
f = open("ram3.txt", "r+")
print(f.read()) # read operation
f.write("Thanks you.\n") # write operation
f.close()

