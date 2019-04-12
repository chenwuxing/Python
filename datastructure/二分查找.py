def binary_search(lis,key):
    low = 0
    high = len(lis) - 1

    while low <= high:
        mid = (low + high) // 2
        if lis[mid] > key:
            high = mid - 1
        elif lis[mid] < key:
            low = mid + 1
        else:
            return mid
    print('目标不存在')
    return 0

def binary_search(list,item):
    first = 0
    last = len(list)-1
    found = False 
    while first <= last and not found:
        mid_pos = (first + last) // 2
        if list[mid_pos] == item:
            found = True
        else:
            if item < list[mid_pos]:
                last = mid_pos - 1
            else:
                first = mid_pos + 1
    return found

#   递归实现
def recursion_binary_search(list,item):
    if len(list) == 0:
        return False
    else:
        mid_pos = len(list) // 2
        if list[mid_pos] == item:
            return True
        else:
            if item < list[mid_pos]:
                return recursion_binary_search(list[:mid_pos],item)
            else:
                return recursion_binary_search(list[mid_pos+1:],item)


print(recursion_binary_search([1,5,7,15,69,70,111],69))

    



