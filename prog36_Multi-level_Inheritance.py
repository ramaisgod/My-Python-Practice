# --- Multilevel Inheritance -----------------

class Dad:
    basketball = 1

class Son(Dad):
    dance = 1
    basketball = 2
    def isdance(self):
        return f"Son can dance {self.dance} times."

class Grandson(Son):
    dance = 6
    def isdance(self):
        return f"Grandson can dance {self.dance} times in a day."

asw = Dad()
awj = Son()
rmz = Grandson()
print(awj.isdance())
print(rmz.basketball)
