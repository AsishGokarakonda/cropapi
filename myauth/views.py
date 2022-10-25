from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from myauth.models import Crop, User
from .serializers import CropSerializer, UserSerializer
import jwt,datetime

# Create your views here.
class RegisterView(APIView):
    def post(self,request):
        serializer= UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class RegisterSuperUserView(APIView):
    def post(self,request):
        # keep is_superuser=True from abstractuser
        request.data['is_superuser']=True
        request.data['name']="Admin"
        serializer= UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class LoginSuperUserView(APIView):
    def post(self,request):
        username=request.data['username']
        password=request.data['password']
        user = User.objects.get(username=username)
        if user is None or user.is_superuser==False:
            return Response({'error':'User not found','status':'failure'})
        if not user.check_password(password):
            return Response({'error':'Password is incorrect','status':'failure'})
        payload={
            'id':user.id,
            # keep token valid for 1 day and refresh if a user logs in again
            'exp':datetime.datetime.utcnow()+datetime.timedelta(days=2),
            'iat':datetime.datetime.utcnow()
        }
        token=jwt.encode(payload,'secret',algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data={
            'jwt':token,
            'status':'success'
        }
        return response
         

class LoginView(APIView):
    def post(self,request):
        username=request.data['username']
        password=request.data['password']

        user=User.objects.filter(username=username).first()
        # if user is not superuser
        if user is None or user.is_superuser==True:
            return Response({'error':'User not found','status':'failure'})
        if not user.check_password(password):
            return Response({'error':'Wrong password','status':'failure'})

        payload={
            'id':user.id,
            # keep token valid for 1 day and refresh if a user logs in again
            'exp':datetime.datetime.utcnow()+datetime.timedelta(days=2),
            'iat':datetime.datetime.utcnow()

        }
        token=jwt.encode(payload,'secret',algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data={
            'jwt':token,
            'status':'success'
        }
        return response

class UserProfileView(APIView):
    def get(self,request):
        # get token from header and decode it to get user id
        token=request.headers['jwt']
        payload=jwt.decode(token,'secret',algorithms=['HS256'])
        user=User.objects.filter(id=payload['id']).first()
        serializer=UserSerializer(user)
        return Response(serializer.data)

class LogoutView(APIView):
    def post(self,request):
        response=Response()
        try:
            response.delete_cookie('jwt')
            response.data={
                'message':'success'
            }
        except:
            response.data={
                'message':'failed'
            }
        return response

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

