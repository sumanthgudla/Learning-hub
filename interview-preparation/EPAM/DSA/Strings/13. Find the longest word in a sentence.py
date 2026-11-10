sentence="Python is awesome"
max_length=0
max_length_word=''
for word in sentence.split():
    if(len(word)>max_length):
        max_length=len(word)
        max_length_word=word
print(max_length_word)

