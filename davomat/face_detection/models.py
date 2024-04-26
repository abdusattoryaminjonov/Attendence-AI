import os

import numpy as np
import cv2

from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

def image_get_face(p,username):

    net = cv2.dnn.readNetFromCaffe(r'C:\Users\asus\OneDrive\Desktop\pbl4\davomat\xml_files\service\deploy.prototxt.txt', r'C:\Users\asus\OneDrive\Desktop\pbl4\davomat\xml_files\service\res10_300x300_ssd_iter_140000.caffemodel')
    
    source_path = p
    target_directory = 'C:/Users/asus/OneDrive/Desktop/pbl4/davomat/'

    image = cv2.imread(source_path)
    print("++++++++++++++++++++++++++++++++++++")
    print(image)
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (160, 160)), 1.0,(160, 160), (104.0, 177.0, 123.0))

    folder_path = "dataset/origin_images/" + username

    net.setInput(blob)
    detections = net.forward()
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        files = os.listdir(folder_path)
        count = len(files)
        print("Number of files in the folder:", count)
    else:
        print("Folder does not exist or is not a directory.")

    for i in range(0, detections.shape[2]):

        confidence = detections[0, 0, i, 2]

        if confidence > 0.5:

            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            # text = "{:.2f}%".format(confidence * 100)
            # y = startY - 10 if startY - 10 > 10 else startY + 10

            face = image[startY:endY, startX:endX].copy()
            faces_resize = cv2.resize(face, (160, 160), interpolation=cv2.INTER_LINEAR)
            save_path = os.path.join(target_directory,folder_path,f"{username}_{count}.jpg")
            # save_path = p
            cv2.imwrite(save_path, faces_resize)
    return faces_resize

class ImageModel(models.Model):
    def photo_upload(self, filename):
        print("============================================")
        print(filename)
        print(self.image.path)
        image = image_get_face(self.image.path,self.user.username)
        return f'uploads/profiles/{self.user.username}/{image}'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    desc = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to=photo_upload)

class AttendanceModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
