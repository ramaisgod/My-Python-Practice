# Dictionary is nothing but it is key value pairs
# d = {} # empty dictionary
# print(type(d))
d1 = {"RMZ": 40000, "ASW": 44000, "AWJ": 56000, "BAV": 41000}
# print(d1)
# print(d1["ASW"]) # print the value of defined key
# d1["VVM"] = 35000 # adding any key and value into original dictionary 
# print(d1)
# del d1["AWJ"]
# print(d1)
# d2 = d1.copy()
# print(d1)
# del d2["BAV"]
# print(d2)
# print(d1.get("ASW"))
# d1.update({"VVM": 29000}) # to add new key and value in original deictionary
# print(d1)
# d1.update({"AAA":{"Name": "Anju", "Age": 26, "Salary": 15000}})  # add dictionary as value 
# print(d1)
# print(d1["AAA"])
# print(d1["AAA"]["Age"])
# d1.update({"ABC": 1234})
# print(d1)
# d1['ABC'] = 4321
# print(d1['ABC'])
# print(d1)
# for key in d1:
#     print(d1[key])


# ------- Practice : Create a own dictionary ----------
# mydict = {}
# q1 = "noun"
# a1 = "A noun is the name of a person, place , animal, or things."
# q2 = "django"
# a2 = "Django is a freamwork to develop web applications with python programming."
# q3 = "oop"
# a3 = "OOP stands for Objects Oriented Programming."
# mydict = {q1:a1, q2:a2, q3:a3}
# print("Enter keywords : ")
# q = input()
# print(mydict[q.lower()])

# mydict = {"2018-12-01": {"Day":1, "For": "Full", "Remarks":"Sunday"},
#             "2018-12-02": {"Day":0, "For": "Half", "Remarks":"Holiday"},
#             "2018-12-03": {"Day":1, "For": "Full", "Remarks":"Tueday"}}
# # for item in mydict.items():
# #     print(item[1]["Remarks"])
# for key,value in mydict.items():
#     print(key, value.get("Remarks"))


a = {11:"ram", 22:"asw"}
print(max(a))
print(type(max(a)))
# inp = int(input("Enter "))
# if inp in a.keys():
#         print(a[inp])






