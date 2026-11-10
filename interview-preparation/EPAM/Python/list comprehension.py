#square all numbers
Input= [1, 2, 3, 4, 5]
squares=[num*num for num in Input]
print(squares)

Input=[10, 15, 20, 25, 30]
even=[num for num in Input if num%2==0]
print(even)

#Extract words having more than 4 characters
Input=['apple', 'cat', 'banana', 'dog', 'mango']
words=[word for word in Input if len(word)>4]
print(words)

#Convert negative numbers to zero, keep positive numbers unchanged
Input= [-2, 5, -8, 10, 0]
nums=[num if num>0 else 0 for num in Input]
print(nums)

#ovwels
Input= 'artificial intelligence'
ovwels=[ch for ch in Input if ch in 'aeiou']
print(','.join(ovwels))

#flatten nested list
Input=[[1, 2], [3, 4], [5, 6]]
nested_list=[col for row in Input for col in row]
print(nested_list)