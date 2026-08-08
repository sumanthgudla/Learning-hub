from pathlib import Path
import json

currentfile=Path(__file__).resolve().parent.parent/'Nested json.json'
with open(currentfile,'r') as f:
    data=json.load(f)
print(data)

def TraverseJson(data):
    if isinstance(data,dict):
        for key,value in data.items():
            TraverseJson(value)
    elif isinstance(data,list):
        for item in data:
            TraverseJson(item)
    else:
        print(data)
TraverseJson(data)