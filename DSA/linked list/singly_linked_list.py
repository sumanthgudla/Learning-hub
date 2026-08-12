from Node import Node

from linked_list import SinglyLinkedList
if __name__ == "__main__":
    linked_list = SinglyLinkedList()
    linked_list.append(10)
    linked_list.append(20)
    linked_list.append(30)
    linked_list.prepend(40)
    print(len(linked_list))


    print("After append:", linked_list)
    linked_list.deleteAtStart()
    linked_list.append(40)
    linked_list.insert(25,0)
    print('before delete',linked_list)
    linked_list.delete(2)




    print("After delete:", linked_list)
    print(linked_list.find(21))


    