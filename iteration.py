class C_Range:
    def __init__(self,start,end,step):
        self.start = start 
        self.end = end
        self.step = step
    
    def __iter__(self):
        return C_Range_Iteration(self.start,self.end,self.step,self.flag)
    
class C_Range_Iteration:
    def __init__(self,start,end,step):
        self.start = start
        self.end = end
        self.step = step
        self.flag = flag

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.start < self.end and self.flag == 0:
            result = self.start
            self.start += self.step
            return result
        elif self.start < self.end and self.flag == -1:
            result = self.end
            self.end -= self.step
            return result
        else:
            raise StopIteration
if __name__ == '__main__':
    for i in C_Range(1,20,2,-1):
        print(i)

            
            
