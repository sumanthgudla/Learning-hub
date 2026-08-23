class Inventory:
    def __init__(self):
        self.products_list=[]
    def add_product(self,id,name,quantity):
        self.products_list.append({"id":id,"name":name,'quantity':quantity})
    def sell_product(self,id,quantity):
        for product in self.products_list:
            if product['id']==id:
                if(product['quantity']>quantity):
                    product['quantity']=product['quantity']-quantity
    def get_stock(self,id):
        for product in self.products_list:
            if product['id']==id:
                return product['quantity']
    def __repr__(self):
        return str(self.products_list)


inventory = Inventory()
inventory.add_product(101, "Laptop", 10)
inventory.add_product(102, "Mouse", 5)
inventory.sell_product(101, 3)

print(inventory.get_stock(101))
# 7

print(inventory)




               
