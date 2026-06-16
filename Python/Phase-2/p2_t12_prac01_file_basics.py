import os
if __name__=='__main__':

    filePath="Python/Phase-2/students.txt"
    with open(filePath,"w") as w:
        w.write("This is sumanth\n")
        w.write("Bharath\n")
        w.write("Charisma\n")
    with open(filePath,"r") as r:
        count=0
        for i in r:
            count+=1
            print(count," ",i,end="")
    with open(filePath,"a") as f:
        f.write("Devendra")
    
    with open(filePath,"r") as f:
        count=0
        for i in f:
            count+=1
        print(count)
            