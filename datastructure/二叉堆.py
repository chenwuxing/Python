class Bin_Heap:
    def __init__(self):
        self.heap_list = [0]
        self.current_size = 0

    def percup(self,i):
        while i //2 > 0:
            if self.heap_list[i] < self.heap_list[i//2]:
                tmp = self.heap_list[i//2]
                self.heaplist[i//2] = self.heaplist[i]
                self.heaplist[i] = tmp
            i = i // 2
    
    def insert(self,k):
        self.heap_list.append(k)
        self.current_size = self.current_size + 1
        self.percup(self.current_size)
    
    def perdown(self,i):
        while (i * 2) <= self.current_size:
            mc = self.min_child(i)
            if self.heap_list[i] > self.heap_list[mc]:
                tmp = self.heap_list[i]
                self.heap_list[i] = self.heap_list[mc]
                self.heap_list[mc] = tmp
            i = mc
    
    def min_child(self,i):
        if i * 2 + 1 > self.current_size:
            return i * 2
        else:
            if self.heap_list[i*2] < self.heap_list[i*2+1]:
                return i * 2
            else:
                return i * 2 + 1
    
    def del_min(self):
        retval = self.heap_list[1]
        self.heap_list[1] = self.heap_list[self.current_size]
        self.current_size = self.current_size -1
        self.heap_list.pop()
        self.perdown(1)
        return retval
    
    def build_heap(self,alist):
        i = len(alist) // 2
        self.current_size = len(alist)
        self.heap_list = [0] + alist[:]
        while(i > 0):
            self.perdown(i)
            i = i - 1







