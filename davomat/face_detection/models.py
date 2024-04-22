from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class ImageModel(models.Model):
    def photo_upload(self, filename):
        return f'uploads/profiles/{self.user.id}/{filename}'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    desc = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to=photo_upload)

class AttendanceModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
