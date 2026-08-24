from pathlib import Path
import json
currentfile=Path(__file__).resolve().parent.parent/'Nested json.json'
with open(currentfile,'r') as f:
    data=json.load(f)

def traverseJson(data):
    if isinstance(data,dict):
        for key,value in data.items():
            if(not isinstance(data,(dict,list))):
                print(key,": ")
            traverseJson(value)
    elif isinstance(data,list):
        for item in data:
            traverseJson(item)
    else:
        print(data)
traverseJson(data)