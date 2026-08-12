from Node import Node
from linked_list import SinglyLinkedList

linked_list = SinglyLinkedList()
linked_list.append(10)
linked_list.append(20)
linked_list.append(30)
linked_list.append(40)
linked_list.append(50)


current_node=linked_list.head
prev_node=None
next_node=current_node
while(current_node.next):
    next_node=current_node.next
    current_node.next=prev_node
    prev_node=current_node
    current_node=next_node
linked_list.head=prev_node


print(linked_list)