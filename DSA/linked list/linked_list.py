from Node import Node
class SinglyLinkedList:
    def __init__(self):
        self.head=None
        self.size=0
    def append(self,value):
        new_node=Node(value)
        self.size+=1
        if self.head is None:
            self.head=new_node
        else:
            current_node=self.head
            while(current_node.next):
                current_node=current_node.next
            current_node.next=new_node
    def __repr__(self):
        current_node=self.head
        data_values=[]
        while(current_node):
            data_values.append(current_node.data)
            current_node=current_node.next
        return ''.join(str(data_values))
    def prepend(self,value):
        self.size+=1
        new_node=Node(value)
        new_node.next=self.head
        self.head=new_node
    def __len__(self):
        return self.size
    def find(self,value):
        current_node=self.head
        while(current_node):
            if value is current_node.data:
                return True
            current_node=current_node.next
        return -1
    def deleteAtStart(self):
        self.head=self.head.next
    def insert(self,value,index):
        if index <0:
            raise ValueError("negative index is not allaowed")
        elif index>self.size:
            raise ValueError(" index is greater than length")
        else:
            if index ==0:
                self.prepend(value)
                return
            self.size+=1
            new_node=Node(value)
            current_node=self.head
            for i in range(index-1):
                current_node=current_node.next
            new_node.next=current_node.next
            current_node.next=new_node
    def delete(self,index):
        if index <0:
            raise ValueError("negative index is not allaowed")
        elif index>self.size:
            raise ValueError(" index is greater than length")
        else:
            if index==0:
                deleteAtStart(self)
                return
            else:
                current_node=self.head
                for i in range(index-1):
                    current_node=current_node.next
                current_node.next=current_node.next.next
                self.size-=1
