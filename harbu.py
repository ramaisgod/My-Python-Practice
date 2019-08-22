# Ctrl + Alt + L
'''
senderid = "ramaisgod@gmail.com"
output = []

email = {"to": ["abc1@gmail.com", "abc2@gmail.com", "abc3@gmail.com", "abc4@gmail.com",
                "abc5@yahoo.in", "abc6@yahoo.in", "abc7@yahoo.in", "b@yahoo.in"],
         "cc ": ["abc1@gmail.com", "abc2@gmail.com", "abc3@gmail.com", "abc4@gmail.com",
                 "abc5@yahoo.in", "abc6@yahoo.in", "abc7@yahoo.in", "b@yahoo.in"]}

print(senderid.split("@")[1])
for key, value in email.items():
    for i in range(len(value)):
        if value[i].split('@')[1] != "gmail.com":
            output.append(value[i])

print(output)
'''

'''
sender_id = "ramaisgod@gmail.com"
email = {"to": ["abc1@gmail.com", "abc2@gmail.com", "abc3@gmail.com", "abc4@gmail.com",
                "abc5@yahoo.in", "abc6@yahoo.in", "abc7@yahoo.in", "b@yahoo.in"],
         "cc ": ["cabc1@gmail.com", "ccabc2@gmail.com", "cbc3@gmail.com", "abc4@gmail.com",

                 "kb5@yahoo.in", "bc6@yahoo.in", "abc7@yahoo.in", "b@yahoo.in"]}

output = []
mydict = {}
for key, value in email.items():
    mydict.update({key: ""})
    for item in value:
        if item.split("@")[1] != sender_id.split("@")[1]:
            output.append(item)
        mydict.update({key: output})

print(mydict)
'''

email = ["ramaisgod@co.in", "harbu@hotmail.com", "anju.harbu@in.com", "abc4@gmail.com",
         "abc5@yahoo.in", "abc6@yahoo.in", "abc7@yahoo.in", "b@yahoo.in",
         "cabc1@gmail.com", "ccabc2@gmail.com", "cbc3@gmail.com", "abc4@gmail.com",
         "kb@yahoo.in", "bc6@yahoo.in", "abc7@yahoo.in", "b@co.in"]

i = 0
for item in email:
    email_p1 = item.split("@")[0][0]
    if len(item.split("@")[0]) > 2:
        email_p2 = "*" * (len(item.split("@")[0]) - 2)
    elif len(item.split("@")[0]) == 2:
        email_p2 = "*"
    else:
        email_p2 = ""

    email_p3 = item.split("@")[0][len(item.split("@")[0]) - 1] if len(item.split("@")[0]) > 2 else ""
    email_p4 = item.split("@")[1][0]
    email_p5 = "*" * (len(item.split("@")[1].split(".")[0]) - 1) if len(item.split("@")[1]) > 2 else "*"
    email_p6 = "." + item.split("@")[1].split(".")[len(item.split("@")[1].split(".")) - 1]
    my_email = f"{email_p1}{email_p2}{email_p3}@{email_p4}{email_p5}{email_p6}"
    email[i] = my_email
    i += 1
print(email)
