import os
import cv2
import time
import numpy as np
import xml.etree.ElementTree as ET

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
            save_dir = output + file + '/'
            if os.path.isdir(self.path + file):     #   判断给定路径下的文件是目录还是文件
                sub_dir = self.path + file + '/'    #   子目录绝对路径
                for im in os.listdir(sub_dir):        
                    img_path = os.path.join(sub_dir + im)
                    img = cv2.imread(img_path)
                    res = cv2.resize(img,size,interpolation = cv2.INTER_CUBIC)
                    if os.path.exists(save_dir):
                        cv2.imwrite(save_dir + im,res)
                    else:
                        os.makedirs(save_dir)
                        cv2.imwrite(save_dir + im,res)
            else:
                img_path = os.path.join(self.path,im)
                img = cv2.imread(img_path)
                res = cv2.resize(img,size,interpolation = cv2.INTER_CUBIC)
                cv2.imwrite(output + im,res)
                

    @time_log
    def get_photo(self,model_path,output):
        """
        功能：使用opencv自带的人脸分类器检测人脸并拍照
        参数:
            1.model_path为人脸分类器的文件路径
            2.output为图像存储位置
        """
        video_capture = cv2.VideoCapture(0)
        num = 0
        while(True):
            ret,frame = video_capture.read()
            face_classifier = cv2.CascadeClassifier(model_path)
            face_rects = face_classifier.detectMultiScale(frame,scaleFactor=1.2,minNeighbors=3,minSize=(32,32))
            if len(face_rects) == 1:
                num += 1
                if num % 10 == 0:
                    #   当output为已经存在的目录时，直接保存图片，否则先创建对应路径的目录，然后保存图片
                    if os.path.exists(output):
                        cv2.imwrite(output + str(num) + '.jpg',frame )
                    else:
                        os.makedirs(output)
                        cv2.imwrite(output + str(num) + '.jpg',frame)
                cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            video_capture.release()
            cv2.destroyAllWindows()

    
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
    
    def img_preprocess(self,img_path,save_path):
        im = cv2.imread(img_path,0)
        # 使用sobel函数进行边缘检测
        im_x = cv2.Sobel(im,cv2.CV_16S,1,0)
        im_y = cv2.Sobel(im,cv2.CV_16S,0,1)
        abs_x = cv2.convertScaleAbs(im_x)
        abs_y = cv2.convertScaleAbs(im_y)
        result = cv2.addWeighted(abs_x,0.5,abs_y,0.5,0)
        result = self.gabor_filter(result)
        _,img_name = os.path.split(img_path)
        cv2.imwrite(save_path + img_name,result)
        
    def gabor(self,ksize,lamda,sigma):
        filters = []
        for theta in np.array([0,np.pi/4,np.pi/2,np.pi*3/4]):
            kernel = cv2.getGaborKernel((ksize,ksize),sigma,theta,lamda,
                                        0.6,0,ktype=cv2.CV_32F)
            filters.append(kernel)
        return filters
        
    def gabor_filter(self,image):
        img_filter = self.gabor(7,8,4)
        for f in img_filter:
            img = cv2.filter2D(image,cv2.CV_8UC3,f)
        return img
        
    

       



        
        
        

if __name__ == '__main__':
    s = Fsolver('G:/xml/')
    for file in os.listdir(s.path):
        sub_dir = s.path + file + '/'
        for xml in os.listdir(sub_dir):
            xml_abs_path = sub_dir + xml
            a = s.analysis_xml(xml_abs_path)
            s.write_xml_info('info.txt',a)







    

    




    




        


    




        