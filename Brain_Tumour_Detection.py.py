# -*- coding: utf-8 -*-
"""BRAIN TUMOUR DETECTION USING ML - PROJECT.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rAiLRcwsn-aRv0fruvTfsRaSEiwjRZRZ
"""

import warnings
warnings.filterwarnings('ignore')

from google.colab import drive
drive.mount('/content/gdrive')

!unzip "/content/gdrive/MyDrive/Clean Data Set.zip"

import numpy as np
import matplotlib.pyplot as plt
import os
import math
import shutil
import glob

#count the number of images in the respective classes
#0-Brain Tumour
#1-Healthy Brain
ROOT_DIR="/content/Clean Data Set"
number_of_images={}

for dir in os.listdir(ROOT_DIR):
  number_of_images[dir] = len(os.listdir(os.path.join(ROOT_DIR,dir)))

number_of_images.items()

os.listdir("/content/Clean Data Set")

len(os.listdir("/content/Clean Data Set"))

"""DATA SPLIT

*   50% for Train Data
*   25% for Testing
*   25% for Validation

"""

def dataFolder(p,split):
  #we create a training folder

  if not os.path.exists("./"+p):
    os.mkdir("./"+p)

  for dir in os.listdir(ROOT_DIR):
    os.makedirs('./'+p+'/'+dir)
    for img in np.random.choice(a=os.listdir(os.path.join(ROOT_DIR,dir)),
                                size=(math.floor(split*number_of_images[dir])-5),
                                replace=False):
     O=os.path.join(ROOT_DIR,dir,img)
     D=os.path.join('./'+p,dir)
     shutil.copy(O,D)
     os.remove(O)
  else:
    print(f"{p}Folder exists")

dataFolder("train",0.5)

dataFolder("val",0.25)

dataFolder("test",0.25)

from keras.layers import  Conv2D,  MaxPool2D, Dropout, Flatten, Dense, BatchNormalization, GlobalAvgPool2D
from keras.models import  Sequential
from keras.preprocessing.image import ImageDataGenerator
import keras

#CNN Model

model=Sequential()

model.add(Conv2D(filters=16, kernel_size=(3,3),activation='relu',input_shape=(224,224,3),padding='same' ))

model.add(Conv2D(filters= 36, kernel_size= (3,3), activation= 'relu' ))
model.add(MaxPool2D(pool_size=(2,2)))

model.add(Conv2D(filters=64, kernel_size=(3,3),activation='relu'))
model.add(MaxPool2D(pool_size=(2,2)))

model.add(Conv2D(filters=128, kernel_size=(3,3),activation='relu'))
model.add(MaxPool2D(pool_size=(2,2)))

model.add(Dropout(rate=0.25))

model.add(Flatten())
model.add(Dense(units=64, activation= 'relu'))
model.add(Dropout(rate= 0.25))
model.add(Dense(units= 1,activation= 'sigmoid'))

model.summary()

model.compile(optimizer='adam', loss= keras.losses.BinaryCrossentropy(),metrics=['accuracy'])

def preprocessingImages1(path):
  """
  input:Path
  output:Pre processed image
  """
  image_data=ImageDataGenerator(zoom_range=0.2,shear_range=0.2,rescale=1/225,horizontal_flip=True)# data Augmentation
  image=image_data.flow_from_directory(directory=path,target_size=(224,224),batch_size=32,class_mode='binary')

  return image

path="/content/train"
train_data=preprocessingImages1(path)

def preprocessingImages2(path):
  """
  input:Path
  output:Pre processed image
  """
  image_data=ImageDataGenerator(rescale=1/225)
  image=image_data.flow_from_directory(directory=path,target_size=(224,224),batch_size=32,class_mode='binary')

  return image

path="/content/test"
test_data=preprocessingImages2(path)

path="/content/val"
val_data=preprocessingImages2(path)

#Early stopping and model check point

from keras.callbacks import ModelCheckpoint, EarlyStopping

#early stopping

es=EarlyStopping(monitor='val_accuracy',min_delta=0.01,patience=10,verbose=1,mode='auto')

#model check point
mc=ModelCheckpoint(monitor='val_accuracy',filepath="./bestmodel.h5",save_best_only=True ,verbose=1,mode='auto')
cd=[es,mc]

hs = model.fit(train_data,
               steps_per_epoch= 8,
               epochs= 30,
               verbose= 1,
               validation_data=val_data,
               validation_steps= 16,
               callbacks= cd)

#Model Graphical Interpretation

h=hs.history
h.keys()

import matplotlib.pyplot as plt

plt.plot(h['accuracy'],c='red')
plt.plot(h['val_accuracy'],c='blue')
plt.title("acc")

plt.show()

import matplotlib.pyplot as plt

plt.plot(h['loss'],c='red')
plt.plot(h['val_loss'])
plt.title('loss')
plt.show()

#model accuracy
from keras.models import load_model
model=load_model("/content/bestmodel.h5")

acc=model.evaluate_generator(test_data)[1]
print(f"the accuracy of our model is {acc*100} %")

from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array

path = '/content/train/no tumour/no_tumour101.jpg'
img=load_img(path,target_size=(224,224))
input_arr=img_to_array(img)/255

plt.imshow(input_arr)
plt.show()

input_arr.shape

input_arr=np.expand_dims(input_arr,axis=0)
y_pred_LogisticRegression=model.predict(input_arr)


if y_pred_LogisticRegression==1:
  print("the MRI is having a Tumour")
else:
  print("the MRI is having no Tumour")

img = '/content/train/tumour/tumour101.jpg'

img_array = np.array(img)
img_array.shape

img_array = img_array.shape(1,150,150,3)
img_array.shape

img = load_img('/content/train/tumour/tumour101.jpg')
plt.imshow(img,interpolation='nearest')
plt.show()

a=model.predict(img_array)
indices = a.argmax()
indices