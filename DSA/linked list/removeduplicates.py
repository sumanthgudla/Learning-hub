from Node import Node
from linked_list import SinglyLinkedList

linked_list = SinglyLinkedList()
linked_list.append(10)
linked_list.append(10)
linked_list.append(10)
linked_list.append(20)
linked_list.append(20)
linked_list.append(30)

current_node=linked_list.head
while(current_node.next):
    if(current_node.data==current_node.next.data):
        print('currentdata',current_node.data,'next node data',current_node.next.data)

        prev_node=current_node
        print('before loop',prev_node.data)
        while(current_node.data==current_node.next.data):
            print('in loop',current_node.data,current_node)
            current_node=current_node.next
        print('after loop',prev_node.data,current_node.data)
       
        prev_node.next=current_node.next
    current_node=current_node.next
print(linked_list)
