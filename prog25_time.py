import time

time_initial = time.time()
n = 0
while(n<100):
    print("While Loop , Number is ", n+1)
    # time.sleep(2) # It waits for 2 seconds
    n += 1
print("Time Taken by While Loop :", time.time()-time_initial, "seconds")

time_initial2 = time.time()
for n in range(100):
    print("For Loop , Number is ", n+1)
    n += 1
print("Time Taken by For Loop :", time.time()-time_initial2, "seconds")

localtime = time.asctime(time.localtime(time.time()))
print(localtime)
print(time_initial)



