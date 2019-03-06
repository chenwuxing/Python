def insert_sort(list):
    for index in range(1,len(list)):

        current_value = list[index]
        position = index

        while position > 0 and list[position-1] > current_value:
            list[position] = list[position-1]
            position = position-1

        list[position] = current_value
    
    return list
a = [4,11,2,1]
print(insert_sort(a))


