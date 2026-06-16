import os
import json
if __name__=="__main__":
    filePath=os.getcwd()+"/Python/Phase-2/logs.txt"
    total_lines=0
    error_lines=0
    with open(filePath,"r") as f:
        for i in f:
            if("error" in i.lower()):
                error_lines+=1
            total_lines+=1
    print(total_lines, error_lines)


    json_txt={
        "error_lines":error_lines
    }
    with open(filePath,"a") as f:
        json.dump(json_txt,f)
    print(json_txt)