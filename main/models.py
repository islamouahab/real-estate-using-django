from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class custom_user(AbstractUser):
    phone_num = models.CharField(max_length=15)
    profile_pic = models.ImageField(upload_to='profile_pics/')

    def __str__(self):
        return self.username
class post(models.Model):
    user_id = models.ForeignKey("custom_user",on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    space = models.FloatField()
    floor_num = models.IntegerField()
    description = models.CharField(max_length=1024)
    price = models.FloatField()
    def __str__(self):
        return self.title
    
class media_files(models.Model):
    post_id = models.ForeignKey("post",on_delete=models.CASCADE)
    path = models.ImageField(upload_to='post_pics/')