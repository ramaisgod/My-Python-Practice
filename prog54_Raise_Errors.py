# Raise In Python
# search Built in exceptions

#----- Example-1 -------
# name = input("Enter Name : ")

# if name.isnumeric():
#     raise Exception("Numbers not allowed")

# print(f"Welcome {name}")

#----- Example-2 -------
# a = int(input("Enter 1st Number: "))
# b = int(input("Enter 2nd Number: "))
# if b==0:
#     raise ZeroDivisionError("Cant not devide by zero !!!")

# result = a/b
# print(result)

#----- Example-3 -------

country = input("Enter Country: ")

try:
    print(age)
except Exception as e:
    if country == "pakistan":
        raise ValueError("pakistan is blocked !!!")

    print("Invalid Input")








