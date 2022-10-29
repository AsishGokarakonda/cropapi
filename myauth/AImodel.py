from cProfile import label
import cv2
import tensorflow as tf
#import matplotlib.pyplot as plt
import numpy as np
import sys
 
path = 'cropapi/myauth/output.txt'
sys.stdout = open(path, 'w')

#Model classifies the picture into the following "classes"
class_names = ['Banana Bacterial Segota', 'Banana Bacterial Wilt', 'Banana Healthy']

#Preprocessing and resizing the image
def prepare(filepath):
    IMG_SIZE = 256  
    img_array = cv2.imread(filepath)  # read in the image
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # resize image to match model's expected sizing
    return new_array.reshape(32, IMG_SIZE, IMG_SIZE, 3)  # return the image with shaping that TF wants.

#loading the ML model
model = tf.keras.models.load_model("cropapi/myauth/BananaModel.h5")

#defining predict function 
#takes in input as a folder of images
def predict(model, img):
    img_array = tf.keras.preprocessing.image.img_to_array(images[i].numpy())
    img_array = tf.expand_dims(img_array, 0)

    predictions = model.predict(img_array)

    predicted_class = class_names[np.argmax(predictions[0])]
    confidence = round(100 * (np.max(predictions[0])), 2)
    return predicted_class, confidence


dataset = tf.keras.preprocessing.image_dataset_from_directory(
    "cropapi/myauth/BananaPictures",
    seed=123,
    shuffle = True, 
    image_size = (256,256),
    batch_size = 32)

#j=1

#plt.figure(figsize=(15, 15))
for images, labels in dataset:
    for i in range(9):
        #ax = plt.subplot(3, 3, i + 1)
        #plt.imshow(images[i].numpy().astype("uint8"))

        predicted_class, confidence = predict(model, images[i].numpy())
        #actual_class = class_names[labels[i]] 

        #print (f"Actual: {actual_class}")
        print (f"Predicted: {predicted_class}.\n")
        print (f"Confidence: {confidence}%\n")
        
        #plt.title(f"Actual: {actual_class},\n Predicted: {predicted_class}.\n Confidence: {confidence}%")
        
        #plt.axis("off")