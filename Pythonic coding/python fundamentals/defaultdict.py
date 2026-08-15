class defaultDict1():
    def __init__(self,default_factory):
        self.dict={}
        self.default_factory=default_factory
    def __getitem__(self,key):
        print(1)
        if key not in self.dict:
            self.dict[key]=self.default_factory
        return self.dict[key]
    def __setitem__(self,key,value):
        self.dict[key]=value

    def __repr__(self):
        return repr(self.dict)

default_list=defaultDict1(int())
default_list['a']=default_list['a']+default_list['a']
print(default_list)

            

