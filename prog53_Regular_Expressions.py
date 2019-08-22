# Regular Expressions  https://www.youtube.com/watch?v=g8u0wLvvPSs&list=PLu0W_9lII9agICnT8t4iYVSZ3eykIAOME&index=87

# List of the metacharacters
# . any charector except newline charector 
# ^ starts with
# $ ends with
# * zero or more occurances
# + one or more occurances
# ? 
# {} Exactly the specified no. of occurances 
# [ ] 
# \ signals a special sequence (can be used to escape special char)
# | either or
# ( ) capture and group

# \d :Matches any decimal digit; this is equivalent to the class [0-9].
# \D :Matches any non-digit character; this is equivalent to the class [^0-9].
# \s :Matches any whitespace character; this is equivalent to the class [ \t\n\r\f\v].
# \S :Matches any non-whitespace character; this is equivalent to the class [^ \t\n\r\f\v].
# \w :Matches any alphanumeric character; this is equivalent to the class [a-zA-Z0-9_].
# \W :Matches any non-alphanumeric character; this is equivalent to the class [^a-zA-Z0-9_].

import re

mytext = '''Reg. Office :
5, 2nd Floor, Dharma Market, Sector - 27,
Opp. SAB Mall, (near Metro Station Sector - 18)
Noida, Gautam Budha Nagar, Uttar Pradesh, 201301, India
Mobile:+91 75202-02200 , 09528468383
Email: director@gloxconsultancy.com , mukeshbabusharma@hotmail.com 
Website:  www.gloxconsultancy.com

Branch Office :
H. No.- 563/B, Sector - F 
Govind Nagar (Near, Mahavidhya Kund / Ratan School)
Mathura, Uttar Pradesh, 281001, India 
Mobile:+91 75202-02200 , 91 9528468383
Email: director@gloxconsultancy.com  , mukeshbabusharma@hotmail.com 
Website:  www.gloxconsultancy.com  
'''

# print(r"\n")  # print \n 

# pattern = re.compile(r'com') 
# pattern = re.compile(r'^Reg. Office')
# pattern = re.compile(r'com$')
#pattern = re.compile(r'co*')
# pattern = re.compile(r'c*o*')
# pattern = re.compile(r'com' '+')
# pattern = re.compile(r'com ' '{2}') # two blank space after com
# pattern = re.compile(r'(-){1}')
# pattern = re.compile(r'(-){1}|:')
# pattern = re.compile(r'\AReg. Office')
# pattern = re.compile(r'\b.com')
# pattern = re.compile(r'83\b')
# pattern = re.compile(r'\d{5}-\d{5}')  # find number like 75202-02200
#pattern = re.compile(r'.(91) \d{10}')
pattern = re.compile(r'([a-zA-Z0-9_.-]+@[a-zA-Z0-9_.-]+\.[a-zA-Z]+)')
# matches = pattern.finditer(mytext)
# for match in matches:
#     print(match.group())
#print(mytext[229:232])
e = re.findall(pattern, mytext)
print(e)







