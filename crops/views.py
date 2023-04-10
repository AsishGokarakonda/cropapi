import time
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from myauth.models import User
from .models import Crop
from .serializers import CropSerializer
import jwt

from cProfile import label
import tensorflow as tf
import numpy as np
import sys
import tensorflow as tf
import numpy as np
import sys
import os
import glob
import re

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
        #save the image to the static/crops folder using os module
        request.data['cropdisease']='tomato_blight'
        # keep only the image name in the database
        # print(request.data['image'])
        # print(request.data['image'].name)
        # request.data['image']=request.data['image'].name
        print(request.data['dayaftersowing'])
        serializer = CropSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            # wait for 5 seconds to save the image to the static folder
            time.sleep(2)
            # # update the cropdisease field in serializer.data and save it to the database
            # # use validated data to save the cropdisease field
            # class_names = ['Banana Bacterial Segota', 'Banana Bacterial Wilt', 'Banana Healthy']

            # #loading the ML model
            # model = tf.keras.models.load_model("crops/BananaModel.h5")

            # dataset = tf.keras.preprocessing.image_dataset_from_directory(
            #     "static/",
            #     shuffle = False, 
            #     image_size = (256,256),
            #     batch_size = 100)


            # #Defining predict function 
            # #Takes in input as model and image
            # def predict(model, img, i):
            #     img_array = tf.keras.preprocessing.image.img_to_array(img)      #Converting PIL Image to numpy array (256,256,3) 
            #     img_array = tf.expand_dims(img_array, 0)                        #Adding 4th Dimension to numpy array (0,256,256,3) 

            #     predictions = model.predict(img_array, verbose = 0)             #Run prediction on the numpy array

            #     predicted_class = class_names[np.argmax(predictions[0])]        #Predicted class is the class with highest probability
            #     # confidence = round(100 * (np.max(predictions[0])), 2)
            #     return predicted_class


            # def sorted_alphanumeric(data):
            #     convert = lambda text: int(text) if text.isdigit() else text.lower()
            #     alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
            #     return sorted(data, key=alphanum_key)


            # # Initializing the predicted outcome to be NULL
            # prediction = "NULL"
            # ImageList = os.listdir("static/crops")
            # ImageList = sorted_alphanumeric(ImageList)
            # # Predicting the disease in the image
            # for images, labels in dataset:
            #     for i in range(len(images)):
            #         if (i==len(images)-1):
            #             Name = ImageList[i]
            #             predicted_class = predict(model, images[len(images) -1].numpy(), len(images) -1)
            #             prediction = predicted_class
            # print("prediction is: ", end="")
            # print (prediction)
            # print(Name)
            
            # do not save the image name in the database
            # add /crops/ to the image name
            # serializer.validated_data['image']='/crops/'+Name






            

            IMG_SIZE = 160

            def Predict_Disease(argument):
                classes = {
                    0: "Aphids",
                    1: "Army Worm",
                    2: "Bacterial blight",
                    3: "Cotton leaf curl",
                    4: "Fussarium wilt",
                    5: "Grey mildew",
                    6: "Healthy",
                    7: "Target Spot"
                }
                return classes.get(argument, "nothing")
            Name = request.data['image']
            print("name is: ", end="")
            print(Name)
            image_path = 'static/crops/'+str(Name)
            unseen_img = tf.keras.preprocessing.image.load_img(image_path,target_size=(IMG_SIZE, IMG_SIZE))
            input_arr = tf.keras.preprocessing.image.img_to_array(unseen_img)
            # convert single image to a batch
            input_arr = np.array([input_arr])  
            input_arr = input_arr.astype('float32') / 255. 

            model = tf.keras.models.load_model("crops/Cotton_Model.h5")
            pred = model.predict(input_arr)
            pred_class = np.argmax(pred, axis=1)
            print(Predict_Disease(int(pred_class)))
            serializer.validated_data['cropdisease']=Predict_Disease(int(pred_class))
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
