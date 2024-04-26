import cv2 , os
import numpy as np
import datetime
import imutils
import pickle
from PIL import Image
from django.conf import settings
from davomat import settings

# net = cv2.dnn.readNetFromCaffe(
#     'xml_files/service/deploy.prototxt.txt', 'xml_files/service/res10_300x300_ssd_iter_140000.caffemodel'
# )

# net = cv2.dnn.readNetFromCaffe(settings.BASE_DIR / 'xml_files/service/deploy.prototxt.txt', settings.BASE_DIR / 'xml_files/service/res10_300x300_ssd_iter_140000.caffemodel')
# net = cv2.dnn.readNetFromCaffe(r'C:\Users\asus\OneDrive\Desktop\pbl4\davomat\xml_files\service\deploy.prototxt.txt', r'C:\Users\asus\OneDrive\Desktop\pbl4\davomat\xml_files\service\res10_300x300_ssd_iter_140000.caffemodel')

# print(net)


videocam = cv2.CascadeClassifier(os.path.join(
    settings.BASE_DIR,'xml_files/haarcascade_frontalface_default.xml'
))

class UploadeImage(object):
    pass

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
                    hoz_flip = cv2.flip(faces_resize, 1)
                    ver_flip = cv2.flip(faces_resize, 0)

                    hoz_flip_path = os.path.join(target_directory, folder_path, f"face_{count}_left_right.jpg")
                    ver_flip_path = os.path.join(target_directory, folder_path, f"face_{count}_top_bottom.jpg")

                    cv2.imwrite(hoz_flip_path, hoz_flip)
                    cv2.imwrite(ver_flip_path, ver_flip)
                    save_path = os.path.join(target_directory, folder_path,f"face_{count}.jpg")
                    print(save_path)
                    cv2.imwrite(save_path, faces_resize)
        else:
            return 
            
        img = cv2.flip(image,1)
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()

class CamerHaac(object):

    def __init__(self):
        self.video = cv2.VideoCapture(0)
        # self.video.set(cv2.CAP_PROP_FRAME_WIDTH,1000)
        # self.video.set(cv2.CAP_PROP_FRAME_HEIGHT,800)

    def __del__(self):
        self.video.release()
        
    def live_frame(self):
        success, image = self.video.read()
        if success:
		

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

class Camera(object):

    def __init__(self):
        self.video = cv2.VideoCapture(0)
        
    
    def __del__(self):
        self.video.release()
        
    def live_frame(self):

        current_datetime = datetime.datetime.now()

        formatted_datetime = current_datetime.strftime('%d-%m-%Y %H:%M:%S')

        file_path = r'C:/Users/asus/OneDrive/Desktop/pbl4/davomat/static/userlist.txt'
        net = cv2.dnn.readNetFromCaffe(r'C:\Users\asus\OneDrive\Desktop\pbl4\davomat\xml_files\service\deploy.prototxt.txt', r'C:\Users\asus\OneDrive\Desktop\pbl4\davomat\xml_files\service\res10_300x300_ssd_iter_140000.caffemodel')
        embedder = cv2.dnn.readNetFromTorch(r'C:/Users/asus/OneDrive/Desktop/pbl4/davomat/dataset/openface_nn4.small2.v1.t7')
        recognizer = pickle.loads(open(r'C:/Users/asus/OneDrive/Desktop/pbl4/davomat/dataset/output/recognizer.pickle', "rb").read())
        le = pickle.loads(open(r'C:/Users/asus/OneDrive/Desktop/pbl4/davomat/dataset/output/le.pickle', "rb").read())

        success, image = self.video.read()

        image = cv2.flip(image,1)

        if success:
            # img = cv2.imread(image)
            img = image

            # ff = img[ start_row : end_row, start_col : end_col]
            
            (h, w) = img.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(img, (160, 160)), 1.0,(160,160), (104.0, 177.0, 123.0))


            net.setInput(blob)
            detections = net.forward()



            for i in range(0, detections.shape[2]):

                confidence = detections[0, 0, i, 2]

                if confidence > 0.51:
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    # text = "{:.2f}%".format(confidence * 100)

                    face = img[startY:endY, startX:endX]
                    (fH, fW) = face.shape[:2]
                    if fW < 20 or fH < 20:
                        continue

                    faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96),
                                             (0, 0, 0), swapRB=True, crop=False)
                    
                    embedder.setInput(faceBlob)
                    vec = embedder.forward()

                    preds = recognizer.predict_proba(vec)[0]
                    j = np.argmax(preds)
                    proba = preds[j]
                    name = le.classes_[j]

                    colorf = (0, 75, 255)

                    
                    if proba < 0.55:
                        name = 'UNKNOWN'
                        colorf = (0, 0, 255)
                    else :
                        with open(file_path, 'r') as f:
                            lines = f.readlines()

                            for line in lines:
                                print("======================================")
                                print(name)
                                # Split the line by commas
                                names = line.strip().split(',')
                                # Check if the name is in the list of names
                                if name in names:
                                    print("Name found in file.")
                                else:
                                     with open(file_path, 'a') as f:
                                        f.write(f"{name},{formatted_datetime}\n")
                    
                    text = "{}: {:.2f}%".format(name, proba * 100)
                    y = startY - 10 if startY - 10 > 10 else startY + 10
                    cv2.rectangle(img, (startX, startY), (endX, endY),
                          colorf, 1)
                    cv2.putText(img, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, colorf, 2)

            ret, jpeg = cv2.imencode('.jpg', img)
            return jpeg.tobytes()
        else:
            return None