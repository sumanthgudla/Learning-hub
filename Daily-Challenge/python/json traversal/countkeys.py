from pathlib import Path
import json
currentfile=Path(__file__).resolve().parent.parent/'Nested json.json'
with open(currentfile,'r') as f:
    data=json.load(f)
count=[0]

def traverseJson(data,total):
    if isinstance(data,dict):
        for key,value in data.items():
            if(not isinstance(value,(dict,list))):
                count[0]=count[0]+1
                print(key,": ",end='')
            traverseJson(value,total)
    elif isinstance(data,list):
        for item in data:
            traverseJson(item,total)
    else:
        print(data)
traverseJson(data,count)
print(count[0])