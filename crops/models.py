from django.db import models
from django.db import models
from myauth.models import User



class Crop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crop_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='crops')
    cropdisease = models.CharField(max_length=100, default='')
    dayaftersowing = models.IntegerField(default=0)