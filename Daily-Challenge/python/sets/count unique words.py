import string
paragraph='''
Find common elements between two lists.
Find elements present in one list but not the other.
Check if all elements are unique.
Find duplicates.
Remove duplicates using a set.
Check whether one set is a subset of another.
Symmetric difference of two sets.
Count unique words in a paragraph.
'''
for ch in string.punctuation:
    paragraph=paragraph.replace(ch,'')
set_words=set(paragraph.lower().split())
print(set_words)
print(len(set_words))