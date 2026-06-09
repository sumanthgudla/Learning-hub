sentences = [
    "Python is a powerful programming language",
    "Senior developers write clean readable code",
    "Programming requires practice and patience"
]
# expected: all unique words > 4 chars, lowercased, sorted


sorted_words= [sorted(set(word.lower() for sentence in sentences for word in sentence.split(' ') if len(word)>4))]
print(sorted_words)