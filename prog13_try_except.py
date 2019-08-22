

try:
    f = open("mylog.txt")
    f2 = open("does_not.txt")
    # num1 = int(input("Enter Number of a "))
    # num2 = int(input("Enter Number of b "))
    # sum = num1 + num2
    # print("Sum of a and b is ",sum)

# except Exception as e:
#     print(e)

except EOFError as e:
    print("EOF Error Occured", e)

except IOError as e:
    print("IO Error Occured", e)

else:
    print("This will run only when except will not execute")

finally:
    f.close()
    print("Welcome to Exception handling.")

