# Extract First Name
def firstname(name):
    try:
        f_name = (name).split()[0]
        return print("First Name = ", f_name)
    except Exception as e:
        print(e)


def middlename(name):
    m_name = (name).split()[1]
    return print("Middle Name = ", m_name)


def lastname(name):
    l_name = (name).split()[-1]
    return print("Last Name = ", l_name)


# name = input("Enter your name : ")
# print(firstname(name), middlename(name), lastname(name))

# ----------- Query -1 -----------------------------------------------
my_string = 'thisIsAGoodBoy'
# pos = [i for i, e in enumerate(my_string+'A') if e.isupper()]
# parts = [my_string[pos[j]:pos[j+1]] for j in range(len(pos)-1)]
# print(pos)
# print(parts)

# ----------- Query -2 -----------------------------------------------
import re
output = re.findall('[a-zA-Z][^A-Z]*', my_string)
print(output)





