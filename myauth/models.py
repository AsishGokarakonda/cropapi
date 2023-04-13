from asyncio.windows_events import NULL
from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    username=models.CharField(max_length=255,unique=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=255,unique=True)
    password=models.CharField(max_length=255)
    is_superuser=models.BooleanField(default=False)
    #if is_superuser is true, then email,name are not required
    REQUIRED_FIELDS = ['name','password']
    USERNAME_FIELD = 'username'

# create class fields for User model. Every User can have many fields and using username as a foreign key to link them
class Field(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    field_name=models.CharField(max_length=100,default=NULL)
    latitude=models.DecimalField(max_digits=9,decimal_places=7,default=NULL)
    longitude=models.DecimalField(max_digits=9,decimal_places=7,default=NULL)
    area = models.FloatField(default=NULL)