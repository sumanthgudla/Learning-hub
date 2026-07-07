def flattend_nested_list(nested_list,res=[]):
    for i in nested_list:
        if type(i) is list:
            flattend_nested_list(i)
        else:
            res.append(i)
    return res

def flattend_nested_list_iterative(nested_list,res=[]):
    stack=nested_list
    while stack:
        item=stack.pop()
        if type(item) is list:
            stack.extend(item)
        else:
            res.append(item)
    return res
            
nested_list=[1,3,[11,12,13],[21,22,23,24,[31,32]],[41]]
print(type(nested_list))
res=flattend_nested_list(nested_list)
res1=flattend_nested_list_iterative(nested_list)
print(res1)



