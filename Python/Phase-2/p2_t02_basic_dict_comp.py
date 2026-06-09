'''Beginner — p2_t02_basic_dict_comp.py
Given a list of words, create a dictionary where each word is the key and the number of vowels in that word is the value.'''
pythonwords = ["python", "developer", "interview", "comprehension"]
vowels='aeiou'
# expected: {'python': 1, 'developer': 4, 'interview': 4, 'comprehension': 5}
python_dict={word : sum(1 for ch in word if ch in vowels) for word in pythonwords }
print(python_dict)