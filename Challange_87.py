
#i = int(input("Enter Number : "))

# while (n<=i):
#     print(n, end=",")
#     n += 1

#print("Invalid Input") if i <=0 else print(",".join(str(n) for n in range(1,i+1)))

#print(",".join(str(n) for n in range(1,i)))

try: 
    i = int(input("Enter Number : "))
    print("Minimum Number should be 1 !!!") if i <=0 else print(",".join(str(n) for n in range(1,i+1))) 
except Exception as e: 
    print("Invalid Input !!!")


