from asyncio.windows_events import NULL
from email.mime import image
from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    username=models.CharField(max_length=255,unique=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=255,unique=True)
    password=models.CharField(max_length=255)
    latitude=models.DecimalField(max_digits=9,decimal_places=7,default=NULL)
    longitude=models.DecimalField(max_digits=9,decimal_places=7,default=NULL)

class Crop(models.Model):
    # this user comes from jwt token from url
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crop_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='crops')
    cropdisease = models.CharField(max_length=100, default='')
