set1=[1,2,3,4,5,6,6,7,7,8]
set_nums=set()
for i in set1:
    if i in set_nums:
        print(i)
    set_nums.add(i)
