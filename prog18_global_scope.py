# ------ Example - 1-------------
'''
a = 10 # This is global variable
def myfunction(b):
    global a  
    a = 50
    # a = 5 # this is local variable
    # b = 10
    print(a,b)

myfunction(33)
print(a)
'''
# ------ Example - 1-------------
def ram1():
    a = 11
    def ram2():
        global a
        a = 22
    print("Before calling ram2()", a)
    ram2()
    print("After calling ram2()", a)

ram1()
