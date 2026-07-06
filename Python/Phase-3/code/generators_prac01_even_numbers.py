def even_numbers():
    start=0
    while start<20:
        yield start
        start+=2
if __name__ =='__main__':
    e=even_numbers()
    for i in e:
        print(i)
  
