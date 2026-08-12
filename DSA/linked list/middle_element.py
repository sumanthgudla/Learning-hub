from Node import Node
from linked_list import SinglyLinkedList

linked_list = SinglyLinkedList()
linked_list.append(10)
linked_list.append(20)
linked_list.append(30)
linked_list.append(40)

slow=linked_list.head
fast=linked_list.head
while(fast and fast.next):
    fast=fast.next.next
    slow=slow.next
print(slow.data)