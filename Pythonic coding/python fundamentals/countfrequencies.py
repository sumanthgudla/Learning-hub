from collections import defaultdict
from pathlib import Path
word_dict=defaultdict(int)

parent_dir = Path(__file__).resolve().parent.parent.parent/'.gitignore'
with open(parent_dir,'r') as f:
    for line in f:
        for word in line.split():
            word_dict[word]=word_dict[word]+1

print(word_dict)
