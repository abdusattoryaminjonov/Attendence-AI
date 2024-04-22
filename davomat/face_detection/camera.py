import cv2 , os
import numpy as np

from django.conf import settings

videocam = cv2.CascadeClassifier(os.path.join(
    settings.BASE_DIR,'xml_files/haarcascade_frontalface_default.xml'
))

class VideoCamera(object):

    def __init__(self):
        self.video = cv2.VideoCapture(0)
    def __del__ (self):
        self.video.release()

    def get_frame(self, k,username):
        count = k

        success , image = self.video.read()
        if success == True:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces_detected = videocam.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
            print(faces_detected)
            for (x, y, w, h) in faces_detected:
                target_directory = 'C:/Users/asus/OneDrive/Desktop/pbl4/davomat/'
                
                face = image[y:y+h, x:x+w]
                faces_resize = cv2.resize(face, (160, 160), interpolation=cv2.INTER_LINEAR)

                folder_path = "dataset/origin_images/" + username
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                
                if count % 10 == 0 :
                    print("ssss")

                    save_path = os.path.join(target_directory, folder_path,f"face_{count}.jpg")
                    print(save_path)
                    cv2.imwrite(save_path, faces_resize)
        else:
            return 
            
        img = cv2.flip(image,1)
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()
