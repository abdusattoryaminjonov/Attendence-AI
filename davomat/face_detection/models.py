import os

import numpy as np
import cv2

from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from PIL import Image
from django.dispatch import receiver



def image_get_face(p,username):
    net = cv2.dnn.readNetFromCaffe(r'C:\Users\Pbl4\pbl4\davomat\xml_files\service\deploy.prototxt.txt', r'C:\Users\Pbl4\pbl4\davomat\xml_files\service\res10_300x300_ssd_iter_140000.caffemodel')
    
    source_path = p
    target_directory = 'C:/Users/Pbl4/pbl4/davomat/'

    image = cv2.imread(source_path)
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (160, 160)), 1.0,(160, 160), (104.0, 177.0, 123.0))

    folder_path = "dataset/origin_images/" + username
    count = 0
    net.setInput(blob)
    detections = net.forward()
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        files = os.listdir(folder_path)
        count = len(files)
        print("Number of files in the folder:", count)
    else:
        os.makedirs(folder_path)
        print("Folder does not exist or is not a directory.")

    for i in range(0, detections.shape[2]):

        confidence = detections[0, 0, i, 2]

        if confidence > 0.5:

            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            face = image[startY:endY, startX:endX].copy()
            faces_resize = cv2.resize(face, (160, 160), interpolation=cv2.INTER_LINEAR)
            
            hoz_flip = cv2.flip(faces_resize, 1)
            ver_flip = cv2.flip(faces_resize, 0)

            img_array = np.array(faces_resize)
            imgcolorg2 = img_array[:,:,2] 
            imgcolorg0 = img_array[:,:,0] 

            hoz_flip_path = os.path.join(target_directory, folder_path, f"face_{count}_left_right.jpg")
            ver_flip_path = os.path.join(target_directory, folder_path, f"face_{count}_top_bottom.jpg")
            imgcolor2_flip_path = os.path.join(target_directory, folder_path, f"face_{count}_color2.jpg")
            imgcolor0_flip_path = os.path.join(target_directory, folder_path, f"face_{count}_color0.jpg")

            cv2.imwrite(imgcolor2_flip_path,imgcolorg2)
            cv2.imwrite(imgcolor0_flip_path,imgcolorg0)
            cv2.imwrite(hoz_flip_path, hoz_flip)
            cv2.imwrite(ver_flip_path, ver_flip)

            save_path = os.path.join(target_directory,folder_path,f"{username}_{count}.jpg")
            # save_path = p
            print(save_path)
            cv2.imwrite(save_path, faces_resize)
    

class ImageModel(models.Model):
    def photo_upload(self, filename):
        # image = image_get_face(self.image.path,self.user.username)
        return f'uploads/profiles/{self.user.username}/{filename}'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    desc = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to=photo_upload)


@receiver(post_save,sender=ImageModel)
def resize_image(sender,instance,created,*args,**kwargs):
    if instance.image:
        image_get_face(instance.image.path, instance.user.username)


class AttendanceModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_came = models.DateTimeField(auto_now_add=True)
    date_out = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('user','date_came')

