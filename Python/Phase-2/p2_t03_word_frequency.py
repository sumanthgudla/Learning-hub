'''Senior level — p2_t03_word_frequency.py
Given a paragraph, build a dictionary of word frequencies — lowercased, punctuation stripped, sorted by frequency (highest first). Use only string methods — no Counter or re.
'''
paragraph = """Python is great. Python is powerful.
               Learning Python is fun. Python developers 
               write clean Python code."""
# expected: {'python': 5, 'is': 3, 'clean': 1, ...}

list_words= paragraph.split()

dict_words={word:sum(1 for word_1 in list_words if word==word_1) for word in set(list_words) }
print(dict_words)