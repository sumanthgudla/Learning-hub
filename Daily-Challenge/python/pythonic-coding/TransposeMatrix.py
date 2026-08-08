nums=[[1,2,3],[4,5,6]]
matrix=[]
for i in range(len(nums[0])):
    new_row=[]
    for j in range(len(nums)):
        new_row.append(nums[j][i])
    matrix.append(new_row)
print(matrix)
matrix2=[[nums[j][i] for j in range(len(nums))] for i in range(len(nums[0]))]
matrix3=zip(*nums)
print(list(matrix3))