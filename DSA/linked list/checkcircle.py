from Node import Node
from linked_list import SinglyLinkedList

linked_list = SinglyLinkedList()
linked_list.append(10)
linked_list.append(20)
linked_list.append(30)
linked_list.append(40)
linked_list.append(50)
new_node=Node(60)
new_node.next=Node(70)
new_node.next.next=Node(80)
new_node.next.next.next=Node(90)
new_node.next.next.next.next=new_node.next

fast=new_node
slow=new_node
iscrcile=False
while(fast and fast.next):
    fast=fast.next.next
    slow=slow.next
    if(slow==fast):
        iscrcile=True
        break

if(iscrcile):
    print('circular loop found')
else :
    print('Normal loop')



