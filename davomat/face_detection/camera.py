import cv2 , os
import numpy as np
import datetime

from django.conf import settings

# net = cv2.dnn.readNetFromCaffe(
#     'xml_files/service/deploy.prototxt.txt', 'xml_files/service/res10_300x300_ssd_iter_140000.caffemodel'
# )

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
                
                if count % 5 == 0 :

                    save_path = os.path.join(target_directory, folder_path,f"face_{count}.jpg")
                    print(save_path)
                    cv2.imwrite(save_path, faces_resize)
        else:
            return 
            
        img = cv2.flip(image,1)
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()

class Camera(object):

    def __init__(self):
        self.video = cv2.VideoCapture(0)
        # self.video.set(cv2.CAP_PROP_FRAME_WIDTH,1000)
        # self.video.set(cv2.CAP_PROP_FRAME_HEIGHT,800)
    
    def __del__(self):
        self.video.release()
        
    def live_frame(self):
        success, image = self.video.read()
        if success:
		# We are using Motion JPEG, but OpenCV defaults to capture raw images,
		# so we must encode it into JPEG in order to correctly display the
		# video stream.

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces_detected = videocam.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
            for (x, y, w, h) in faces_detected:

                # face = image[y:y+h, x:x+w]
                # faces_resize = cv2.resize(face, (160, 160), interpolation=cv2.INTER_LINEAR)

                cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
            frame_flip = cv2.flip(image,1)
            ret, jpeg = cv2.imencode('.jpg', frame_flip)
            return jpeg.tobytes()
        else:
            return None