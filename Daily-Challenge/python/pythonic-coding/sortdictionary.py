dictionay=[{
    'name':'Sum',
    'age':5
},
{
    'name':'Sam',
    'age':56
}
]
sorted_keys=sorted(dictionay, key=lambda x: x['age'])
print(sorted_keys)

sort_nums=[[1,3],[2,4],[1,2]]
sorted_nums=sorted(sort_nums,key= lambda x : x[0])
print(sorted_nums)