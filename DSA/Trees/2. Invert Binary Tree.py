from TreeNode import TreeNode
root = TreeNode(10)

root.left = TreeNode(5)
root.right = TreeNode(20)

root.left.left = TreeNode(3)
root.left.right = TreeNode(7)

root.right.right = TreeNode(30)

def Invert(root):
    if root is None:
        return 
    temp=root.left
    root.left=root.right
    root.right=temp
    Invert(root.left)
    Invert(root.right)

def Traversal(Node):
    if Node is None:
        return
    print(Node.val)
    Traversal(Node.left)
    Traversal(Node.right)

Traversal(root)
Invert(root)
print()
Traversal(root)
