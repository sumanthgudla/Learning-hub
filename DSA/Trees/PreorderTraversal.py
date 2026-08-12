from TreeNode import TreeNode
root = TreeNode(10)

root.left = TreeNode(5)
root.right = TreeNode(20)

root.left.left = TreeNode(3)
root.left.right = TreeNode(7)

root.right.right = TreeNode(30)


def Traversal(Node):
    if Node is None:
        return
    print(Node.val)
    Traversal(Node.left)
    Traversal(Node.right)



if __name__=='__main__':
    Traversal(root)
