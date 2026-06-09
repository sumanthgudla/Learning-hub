'''Slightly harder — t05_word_tools.py
Given the sentence below:

Split it into a list of words
Print how many words there are using len()
Join the words back together separated by " - "
Print the final joined string

pyth'''
sentence = "Python is fun to learn"
# your code here
words_list=sentence.split(' ')
print(words_list)
print(len(words_list))
sentenc_back="-".join(words_list)
print(sentenc_back)