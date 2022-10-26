from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from myauth.models import User
from .models import Crop
from .serializers import CropSerializer
import jwt

# Create your views here.
class CropListView(APIView):
    def get(self,request):
        # get jwt token from header and decode it to get user id and save it to crop model
        token=request.headers['jwt']
        payload=jwt.decode(token,'secret',algorithms=['HS256'])
        user=User.objects.filter(id=payload['id']).first()
        crops=Crop.objects.filter(user=user)
        # truncate the image field string to get only last part of the path
        # for crop in crops:
        #     print(crop.image.name)
        #     crop.image= crop.image.name.rsplit('/', 1)[1]
        serializer=CropSerializer(crops,many=True)
        return Response(serializer.data)


class CropView(APIView):
    def post(self,request):
        # get jwt token from header and decode it to get user id and save it to crop model
        token=request.headers['jwt']
        payload=jwt.decode(token,'secret',algorithms=['HS256'])
        user=User.objects.filter(id=payload['id']).first()
        request.data['user']=user.id
        # a ml model will be used to predict the disease and update the cropdisease field
        request.data['cropdisease']='tomato_blight'
        # keep only the image name in the database
        print(request.data['image'])
        print(request.data['image'].name)
        # request.data['image']=request.data['image'].name
        serializer = CropSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data)
            # return in array format to be used in the frontend
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
