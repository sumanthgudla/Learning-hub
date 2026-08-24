from pathlib import Path
import json
currentfolder=Path(__file__).resolve()
parent_dir=currentfolder.parent.parent
file_path=parent_dir/"Nested json.json"
with open(file_path,'r') as f:
    data=json.load(f)
def TraverseJson(data):
    if isinstance(data,dict):
        for key,value in data.items():
            print(key)
            TraverseJson(value)
    elif isinstance(data,list):
        for item in data:
            TraverseJson(item)
    else:
        pass
TraverseJson(data)