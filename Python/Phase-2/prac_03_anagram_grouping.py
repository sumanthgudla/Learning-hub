'''prac_03_anagram_grouping.py
Group words that are anagrams of each other into a dict where key is the sorted letters and value is list of anagram words.
'''
words = ["eat", "tea", "tan", "ate", "nat", "bat"]
# expected: {'aet': ['eat', 'tea', 'ate'], 
#            'ant': ['tan', 'nat'], 
#            'abt': ['bat']}


dicts_words={''.join(sorted(word)) :[j for j in words if sorted(word) == sorted(j)] for word in words}
print(dicts_words)