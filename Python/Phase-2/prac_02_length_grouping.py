words = ["cat", "dog", "elephant", "ant", "python", "rat", "java"]
# expected: {3: ['cat', 'dog', 'ant', 'rat'], 6: ['python'], 
#            4: ['java'], 8: ['elephant']}

dicts_words={len(word) :[i for i in words if(len(word)==len(i))] for word in words}
print(dicts_words)