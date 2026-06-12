class BankAccount:
    def __init__(self,owner,balance=0):
        self.balance=balance
        self.owner=owner
    def deposit(self,amount):
        self.balance=self.balance+amount
    def withdraw(self,amount):
        if(self.balance-amount<0):
            raise ValueError("Amount cannot be deductable")
        else:
            self.balance=self.balance-amount
    def getBalance(self):
        print(f"The {self.owner} balnce is {self.balance}")
    def __str__(self):
        return (f"Account[{self.owner}]: {self.balance}")


if __name__ == "__main__":
    P1=BankAccount("Sumanth")
    P2=BankAccount("Bharath",50)
    P1.deposit(5000)
    P1.withdraw(2000)
    P1.withdraw(8000)
    print(P1)
    



