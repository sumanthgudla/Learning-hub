def flattenList(data):
    res=[]
    for i in data:
        if isinstance(i,list):
            res.extend(flattenList(i))
        else:
            res.append(i)
    return res


data = [1, [2, 3], [4, [5, [6, 7]]], [[[8, 9], 10]]]
print(flattenList(data))


