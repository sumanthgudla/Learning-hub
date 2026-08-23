from TreeNode import TreeNode
root = TreeNode(10)

root.left = TreeNode(5)
root.right = TreeNode(20)

root.left.left = TreeNode(3)
root.left.right = TreeNode(7)

root.right.right = TreeNode(30)

def MaximumDepth(root):
    if root is None:
        return 0
    print(root.val)
    left=MaximumDepth(root.left)
    right=MaximumDepth(root.right)
    return 1+max(left,right)
maxvalue=MaximumDepth(root)
print(maxvalue)