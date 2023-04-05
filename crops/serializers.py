from rest_framework import serializers

from .models import Crop
class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model=Crop
        fields=['id','user','crop_name','image','cropdisease','dayaftersowing']