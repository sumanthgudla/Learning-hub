numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# map result:    [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
# filter result: [25, 36, 49, 64, 81, 100]


square_list=list(filter(lambda x: x>20,map(lambda x : x*x,numbers)))
print(square_list)