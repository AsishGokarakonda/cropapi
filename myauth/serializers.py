from rest_framework import serializers

# from .models import Crop
from .models import User,Field

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','name','email','password','is_superuser']
        # THIS IS THE LINE THAT MAKES THE PASSWORD NOT VISIBLE
        extra_kwargs={'password':{'write_only':True}}
        
    def create(self,validated_data):
        password=validated_data.pop('password',None)
        instance=self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

# class CropSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Crop
#         fields=['id','user','crop_name','image','cropdisease']

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model=Field
        fields=['id','user','field_name','crop_name','latitude','longitude','area','start_date','start_day','cur_day','coordinates']  
