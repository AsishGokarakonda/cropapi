# making prediction
# with tf.device('/device:GPU:1'):
import tensorflow as tf
import numpy as np

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

image_path = 'Cotton_Test/Healthy/10.jpg'
unseen_img = tf.keras.preprocessing.image.load_img(image_path,target_size=(IMG_SIZE, IMG_SIZE))
input_arr = tf.keras.preprocessing.image.img_to_array(unseen_img)
# convert single image to a batch
input_arr = np.array([input_arr])  
input_arr = input_arr.astype('float32') / 255. 

model = tf.keras.models.load_model('Cotton_Model.h5')
pred = model.predict(input_arr)
print (pred)
# predicting class
pred_class = np.argmax(pred, axis=1)
print(Predict_Disease(int(pred_class)))
