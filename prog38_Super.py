# ---- Super() and Overriding In Classes ---------

class A:
    var_A = "I am a class variable in class A."
    def __init__(self):
        self.var1 = "I am var1 variable inside class A's constructor."
        self.var_A = "Instance variable in class A"
        self.var_special = "I am special variable in class A"


class B(A):
    var_B = "I am a class variable in class B."
    def __init__(self):
        super().__init__()
        self.var2 = "I am var2 variable inside class B's constructor."
        self.var_A = "Instance variable in class B"
        #super().__init__()

a = A()
b = B()

print(b.var_A)
print(b.var_special)
print(b.var2)
print(b.var_A)
