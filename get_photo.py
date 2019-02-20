import cv2



def get_photo(model_path,photo_pos):
    """
    实现自动拍照功能
    参数：
    model_path:人脸检测模型的文件路径
    photo_pos:图片的保存路径

    """
    video_capture = cv2.VideoCapture(0)
    c = 0
    while(True):
        ret,frame = video_capture.read()
        face_classifier = cv2.CascadeClassifier(model_path)
        faceRects = face_classifier.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
        if len(faceRects) == 1:
            c += 1
            if c % 10 == 0:
                cv2.imwrite(photo_pos + str(c) + '.jpg',frame)
            cv2.imshow('frame',frame)
        #   按q键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # 释放窗口资源
    video_capture.release()
    cv2.destroyAllWindows()




