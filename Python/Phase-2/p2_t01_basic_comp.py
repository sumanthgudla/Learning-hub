'''Beginner — p2_t01_basic_comp.py
Using a list comprehension, create a list of all numbers from 1 to 50 that are divisible by 3 but not by 9. Print the result.
'''

list_nums=[x for x in range(1,50) if x%3==0 and x%9!=0]
print(list_nums)