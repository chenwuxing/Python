import os
import cv2
import time

def time_log(func):
    """
    功能：计时功能,装饰类内方法

    """
    def wrapper(self,*args,**kwargs):
        start_time = time.time()
        func(self,*args,**kwargs)
        stop_time = time.time()
        print('spend time：{}s'.format(stop_time-start_time))
    return wrapper





class Fsolver():
    def __init__(self,path):
        self.path = path

    @time_log
    def resize(self,output,size):
        """
        功能：对图片的尺寸进行调整,能够适应给定目录下还有子目录的情况
        参数：
            size:调整后的图片尺寸
            output:图片保存位置，output目录的形式应为'a:/b/'

        """
        for file in os.listdir(self.path):
            if os.path.isdir(self.path + file):     #   判断给定路径下的文件是目录还是文件
                sub_dir = self.path + file + '/'    #   子目录绝对路径
                for im in os.listdir(sub_dir):      #   
                    img_path = os.path.join(sub_dir + im)
                    img = cv2.imread(img_path)
                    res = cv2.resize(img,size,interpolation = cv2.INTER_CUBIC)
                    if os.path.exists(output):
                        cv2.imwrite(output + im,res)
                    else:
                        os.makedirs(output)
                        cv2.imwrite(output + im,res)
            else:
                img_path = os.path.join(self.path,im)
                img = cv2.imread(img_path)
                res = cv2.resize(img,size,interpolation = cv2.INTER_CUBIC)
                cv2.imwrite(output + im,res)
    
    def rename(self,output):
        """
        功能：重命名文件
        参数：
            output:图片保存位置
        """
        for file in os.listdir(self.path):
            if os.path.isdir(self.path + file):
                sub_dir = self.path + file + '/'
                for im in os.listdir(sub_dir):
                    pass
            
            else:
                img_path = os.path.join(self.path,im)
                img = cv2.imread(img_path)




    

    




    




        


    




        