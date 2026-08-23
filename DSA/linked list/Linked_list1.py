from Node1 import Node
class LinkedList1:
    def __init__(self):
        self.head=None
        self.size=0
    def add(self,value):
        new_node=Node(value)
        if self.head is None:
            self.head=new_node
        else:
            temp_node=self.head
            while(temp_node.next!=None):
                temp_node=temp_node.next
            temp_node.next=new_node
    def __repr__(self):
        temp_node=self.head
        data_values=[]
        while(temp_node!=None):
            data_values.append(temp_node.value)
            temp_node=temp_node.next
        return "".join(str(data_values))
    def reverse(self):
        prev=None
        curr=self.head
        while(curr!=None):
            next=curr.next
            curr.next=prev
            prev=curr
            curr=next
        self.head=prev





linkedList=LinkedList1()
linkedList.add(1)
linkedList.add(2)
linkedList.reverse()
print(linkedList)
