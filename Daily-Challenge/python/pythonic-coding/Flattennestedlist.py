nums=[1,2,3,4,5,[1,2,3,[1,2],3],5]
def flattennestedList(nums,res):
    for i in nums:
        if type(i) is list:
            flattennestedList(i,res)
        else:
            res.append(i)
    return res

response=flattennestedList(nums,[])
print(response)