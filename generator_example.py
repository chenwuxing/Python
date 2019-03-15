def fun():
    for i in range(20):
        x=yield i
        print('good',x)

        

if __name__ == '__main__':
    for x in fun():
        print(x)