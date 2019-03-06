def select_sort(list):
    for compar_num in range(len(list)-1,0,-1):
        max_pos = 0
        for index in range(1,compar_num + 1):
            if list[index] > list[max_pos]:
                max_pos = index

        list[compar_num],list[max_pos] = list[max_pos],list[compar_num]
    
    return list

a= [2,1,4,3,5,5,2]
print(select_sort(a))




