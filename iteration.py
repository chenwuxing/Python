class C_Range:
    def __init__(self,start,end,step):
        self.start = start 
        self.end = end
        self.step = step
    
    def __iter__(self):
        return C_Range_Iteration(self.start,self.end,self.step)
    
class C_Range_Iteration:
    def __init__(self,start,end,step):
        self.start = start
        self.end = end
        self.step = step

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.start < self.end:
            result = self.start
            self.start += self.step
            return result
        else:
            raise StopIteration
if __name__ == '__main__':
    for i in C_Range(1,20,1):
        print(i)

            
            
