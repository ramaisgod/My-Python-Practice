# Json Module

import json
# ---- Example -1 
data = '{"name": "Ram Krishna", "age":"30"}'
print(data)
pars = json.loads(data)
print(pars)
print(type(pars))
print(pars['age'])

# ---- Example -2

data2 = {
    "company": "Seynse Technology",
    "employee": ['Vijay', 'Vinod', 'Ram', 'Amitabh', 'Niranjan'],
    "client_name": ('Airtel', 'Vodafone', 'HDFC')
}

mydata2 = json.dumps(data2, sort_keys=True) # It will convert data into java script compatible 
print(mydata2)

# ---- Example -2 
with open("emp.json") as f:
    data = json.load(f)

print(data)
print(data['course'])
print(data['course']['Python'])
print(data['course']['Python']['fees'])


