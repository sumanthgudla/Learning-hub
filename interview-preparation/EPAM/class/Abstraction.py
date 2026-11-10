import math
class Shape:
    def area(self):
        pass

class Circle(Shape):
    def __init__(self,r):
        super().__init__()
        self.r=r
    def area(self):
        return math.pi*self.r*self.r


class Rectange(Shape):
    def __init__(self,length,breadth):
        super().__init__()
        self.length=length
        self.breadth=breadth
    def area(self):
        return self.length*self.breadth

A=Rectange(5,2)
print(A.area())




