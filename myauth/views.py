from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from myauth.models import  User, Field
# from .models import Crop
from .serializers import UserSerializer,FieldSerializer
# from .serializers import CropSerializer
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
        try:
            username=request.data['username']
            password=request.data['password']
            try:
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
            except:
                return Response({'error':'User not found','status':'failure'})
        except:
            return Response({'error':'Username and password are required','status':'failure'})
         

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

class checkJwtValidatedView(APIView):
    def get(self,request):
        try:
            token=request.headers['jwt']
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
            user=User.objects.filter(id=payload['id']).first()
            if user is None:
                return Response({'status':'failure','error':'User not found'})
            else:
                return Response({'status':'success'})
        except:
            #401 means unauthorized
            return Response({'status':'failure','error':'Invalid token'},status=401)

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

# get all user details for admin
class UserListView(APIView):
    def get(self,request):
        # get jwt token from header and decode it to get user id and save it to crop model
        token=request.headers['jwt']
        payload=jwt.decode(token,'secret',algorithms=['HS256'])
        user=User.objects.filter(id=payload['id']).first()
        if user.is_superuser==False:
            return Response({'error':'Not allowed','status':'failure'})
        users=User.objects.all()
        serializer=UserSerializer(users,many=True)
        return Response(serializer.data)

#get latitude and longitude of all the users for admin
class UserLocationView(APIView):
    def get(self,request):
        # get jwt token from header and decode it to get user id and save it to crop model
        token=request.headers['jwt']
        payload=jwt.decode(token,'secret',algorithms=['HS256'])
        user=User.objects.filter(id=payload['id']).first()
        if user.is_superuser==False:
            return Response({'error':'Not allowed','status':'failure'})
        allfields=Field.objects.all()
        serializer=FieldSerializer(allfields,many=True)
        return Response(serializer.data)


class AddFieldView(APIView):
    def post(self,request):
        # get jwt token from header and decode it to get user id and save it to crop model
        token=request.headers['jwt']
        payload=jwt.decode(token,'secret',algorithms=['HS256'])
        user=User.objects.filter(id=payload['id']).first()
        if user.is_superuser==False:
            # add field to user. We get user id from jwt token
            #check if we can convert area to float
            try:
                request.data['area']=float(request.data['area'])
            except:
                # status code 400 means bad request
                return Response({'error':'Area must be a number','status':'failure'},status=400)
            if request.data['area']<=0:
                # status code 400 means bad request
                return Response({'error':'Area must be greater than 0','status':'failure'},status=400)
            if request.data['latitude'] is None or request.data['longitude'] is None:
                # status code 400 means bad request
                return Response({'error':'Latitude and longitude are required','status':'failure'},status=400)
            request.data['user']=user.id
            serializer=FieldSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                # status code 500 means internal server error
                return Response(serializer.errors,status=500)
        else:
            # status code 403 means forbidden
            return Response({'error':'Not allowed','status':'failure'},status=403)