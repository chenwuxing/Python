from dequeue import Deque

def palindrome_check(word):
    d = Deque()
    for letter in word:
        d.add_rear(letter)
    word_len = len(word)
    
    equal = True
    while d.size() > 1 and equal:
        front_element = d.remove_front()
        rear_element = d.remove_rear()
        if front_element != rear_element:
            equal = False
    
    return equal 
print(palindrome_check('rvasar'))
        

        



