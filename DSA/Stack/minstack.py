class minStack:
    def __init__(self):
        self.stack_list=[]
    def append(self,newelement):
        self.stack_list.append(newelement)
    def pop(self):
        self.stack_list.pop()