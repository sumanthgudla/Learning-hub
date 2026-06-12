class Shape():
    def __init__(self):
        pass
    def area(self):
        return 0

class Rectangle(Shape):
    def __init__(self,length,breadth):
        self.length=length
        self.breadth=breadth
        self.area()
    def area(self):
        super().area()
        return self.length*self.breadth

class Circle(Shape):
    pi=3.14
    def __init__(self,radius):
        self.radius=radius
        self.area()
    def area(self):
        return Circle.pi*self.radius*self.radius


if __name__=='__main__':
    shapes = [Rectangle(4, 5), Circle(3), Rectangle(2, 2)]
    area=[shape.area() for shape in shapes]
    print(sum(area))

