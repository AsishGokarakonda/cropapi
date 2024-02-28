from django.db import models
from django.db import models
from myauth.models import User



class Market(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
