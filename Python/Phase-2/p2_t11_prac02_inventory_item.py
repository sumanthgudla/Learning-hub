class InventoryItem():
    def __init__(self,name,price,quantity):
        self.__name = name
        self.price = price
        self.quantity = quantity
    
    @property
    def name(self):
        return self.__name
    
    @property
    def price(self):
        return self.__price
    
    @property
    def quantity(self):
        return self.__quantity
    
    @price.setter
    def price(self,value):
        if value<0:
            raise ValueError("Price cannot be less than zero")
        else:
            self.__price=value
    
    @quantity.setter
    def quantity(self,value):
        if value<0:
            raise ValueError("quantity cannot be less than 0")
        else:
            self.__quantity=value
    
    @property
    def total_value(self):
        return self.price*self.quantity
    
    def __repr__(self):
        return f"quantity : {self.quantity}"
    

if __name__ =='__main__':
    I=InventoryItem("widget",50,6)
    print(I.price)
    print(I.total_value)
    print(I)


