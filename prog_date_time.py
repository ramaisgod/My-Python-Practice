import datetime

# -----------------------
d = '23/12/2018'

print(type(datetime.datetime.strptime(d[:10], '%d/%m/%Y').date()))
d1 = datetime.datetime.strptime(d[:10], '%d/%m/%Y').date()
print(d1.day)
# print(datetime.datetime.now().date())
# -----------------------
# datetime.datetime.strptime(datetime.datetime.today(), "%Y-%m-%d").date())

# datetime.strptime(d3, "%Y-%m-%d").date()

import time
#d2 = datetime.datetime.today()
#print(datetime.datetime.strptime(str(d2), "%Y-%m-%d").date)
# import sys
# import time
# for i in range(10,0,-1):
#     sys.stdout.write("\r")
#     sys.stdout.write("{:2d}".format(i))
#     sys.stdout.flush()
#     time.sleep(1)


# for remaining in range(10, 0, -1):
#     sys.stdout.write("\r")
#     sys.stdout.write("{:2d} seconds remaining.".format(remaining))
#     sys.stdout.flush()
#     time.sleep(1)

# sys.stdout.write("\rComplete!            \n")

