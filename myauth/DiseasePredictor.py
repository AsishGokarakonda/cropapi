from cProfile import label
import tensorflow as tf
import numpy as np
import sys
import os
import glob
import re

# File where output is sent
path = 'myauth/output.txt'
sys.stdout = open(path, 'w')

#Model classifies the picture into the following "classes"
class_names = ['Banana Bacterial Segota', 'Banana Bacterial Wilt', 'Banana Healthy']

#loading the ML model
model = tf.keras.models.load_model("myauth/BananaModel.h5")


dataset = tf.keras.preprocessing.image_dataset_from_directory(
    "myauth/BananaPictures",
    shuffle = False, 
    image_size = (256,256),
    batch_size = 1000000000)


#Defining predict function 
#Takes in input as model and image
def predict(model, img, i):
    img_array = tf.keras.preprocessing.image.img_to_array(img)      #Converting PIL Image to numpy array (256,256,3) 
    img_array = tf.expand_dims(img_array, 0)                        #Adding 4th Dimension to numpy array (0,256,256,3) 

    predictions = model.predict(img_array, verbose = 0)             #Run prediction on the numpy array

    predicted_class = class_names[np.argmax(predictions[0])]        #Predicted class is the class with highest probability
    # confidence = round(100 * (np.max(predictions[0])), 2)
    return predicted_class


def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)


# Initializing the predicted outcome to be NULL
prediction = "NULL"
ImageList = os.listdir("myauth/BananaPictures/Banana Healthy")
ImageList = sorted_alphanumeric(ImageList)
# Predicting the disease in the image
for images, labels in dataset:
    for i in range(len(images)):
        if (i==len(images)-1):
            Name = ImageList[i]
            predicted_class = predict(model, images[len(images) -1].numpy(), len(images) -1)
            prediction = predicted_class


print (prediction)
print(Name)