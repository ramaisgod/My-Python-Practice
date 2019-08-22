import datetime
from datetime import datetime
from datetime import timedelta
d1 = datetime.today()
# d2 = datetime(2018, 12, 1)
# day_count = (d2 - d1).days + 1
# print(day_count)
# for d in range(day_count):
#     print(d1 + timedelta(days=d))

# while d1>=d2:
#     print(d1 + timedelta(days=1))

# d3 = '2017-12-31'
# d4 = datetime.strptime(d3, "%Y-%m-%d").date()
# print(d4.year)
# print(d4)
# leave_start = '2018-12-20'
# leave_end = '2018-12-25'
# leave_start = datetime.strptime(leave_start, "%Y-%m-%d")
# leave_end = datetime.strptime(leave_end, "%Y-%m-%d")
# days_count = (leave_end.date() - leave_start.date()).days + 1
# print(days_count)
# print(type(leave_start))

# for leave in range(days_count):
#     myleave = timedelta(days=leave) + leave_start # add 1 day in date
#     print(myleave)
#     # print(timedelta(days=leave))

# # tot_months = (leave_end.year - leave_start.year)*12 + leave_end.month - leave_start.month
# # print(tot_months)
# # print(leave_end.weekday())
# for a in range(5):
#     b = 10 + a
#     print(b)

# ------------------------------------ 

# print(datetime.datetime.today().replace(microsecond=0))


# ---- below function create a new date as EMI date
from dateutil import relativedelta

def first_emi(date):
    day_of_date = int(date.strftime("%d"))
    if day_of_date < 21:
        first_emi_date = date + relativedelta.relativedelta(months=1)
    else:
        first_emi_date = date + relativedelta.relativedelta(months=2)
    first_emi_date = first_emi_date.replace(day=5)
    return first_emi_date

mydate = datetime(2018, 12, 1)
print(first_emi(mydate))


def last_emi(pd_date):
    day_of_date = int(pd_date.strftime("%d"))
    if day_of_date < 5:
        last_emi_date = pd_date - relativedelta.relativedelta(months=1)
    else:
        last_emi_date = pd_date
    last_emi_date = last_emi_date.replace(day=5)
    return last_emi_date
