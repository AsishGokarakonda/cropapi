from email.mime import image
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    username=models.CharField(max_length=255,unique=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=255,unique=True)
    password=models.CharField(max_length=255)

class Crop(models.Model):
    # this user comes from jwt token from url
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crop_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/crops')
    cropdisease = models.CharField(max_length=100, default='')
