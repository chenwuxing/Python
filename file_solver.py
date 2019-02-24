import os
import cv2

class Fsolver():
    def __init__(self,path):
        self.path = path
    
    def resize(self,size,output):
        """
        功能：对图片的尺寸进行调整
        参数：
            size:调整后的图片尺寸
            output:图片保存位置
        """
        for im in os.listdir(self.path):
            img_path = os.path.join(self.path,im)
            img = cv2.imread(img_path)
            res = cv2.resize(img,size)
            cv2.imwrite(output + im,res)
    
    def rename(self,output):
        """
        功能：重命名文件
        参数：
            output:图片保存位置
        """
        for im in os.listdir(self.path):
            img_path = os.path.join(self.path,im)
            img = cv2.imread(img_path)
            ren = cv2.rename()


    




        