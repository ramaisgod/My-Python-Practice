# --- Abstract Base Class & @abstractmethod ----
# it will force declare a particular function inside all child class  

# from abc import ABCMeta, abstractmethod   # for below python version 3.4
from abc import ABC, abstractmethod  # for above 3.5

class Shape(ABC):
    @abstractmethod
    def printarea(self):
        return 0

class Rectangle(Shape):
    type = "Rectangle"
    sides = 4
    def __init__(self):
        self.length = 6
        self.breath = 7
    
    def printarea(self):
        return self.length * self.breath

rect1 = Rectangle()
print(rect1.printarea())
# we can not create instance object of Abstract class
# obj_shape = Shape()

