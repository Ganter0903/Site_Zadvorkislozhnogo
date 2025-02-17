from django.db import models

class Users(models.Model):
    UserName = models.CharField(max_length=255)
    UserPhoto = models.ImageField(upload_to="photos/%Y/%m/%d/")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
