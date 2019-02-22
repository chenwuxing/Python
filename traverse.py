import os
import cv2


def timer(func):
    def wrapper(*args,**kwargs):
        start_time = time.time()
        func(*args,**kwargs)
        stop_time = time.time()
        print("处理图片共耗时:{}s".format(stop_time-start_time))
    return wrapper

@timer
def traverse_files(outer_file): #   outer_file的形式应该像'D:/a/'
    for inner_files in os.listdir(outer_file):  # 此时可以得到包含内层文件夹名称的列表
        inner_files_path = outer_file + inner_files + '/'   #得到内部文件夹的路径
        for item in os.listdir(inner_files_path):   # 得到一个包含内部文件夹文件的列表，遍历这个列表
            img_path = inner_files_path + item
            img = cv2.imread(img_path)
            res = cv2.resize(img,(64,64),interpolation = cv2.INTER_CUBIC)
            cv2.imwrite('G:/test/' + inner_files + '_' + item,res)













