# -*- coding: utf-8 -*-
"""RockPaperScisors.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fkDJH21UVte8g-E7N0rdnCjxQB1hgsm5
"""

# import tensorflow
import tensorflow as tf
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# print tensorflow version
print(tf.__version__)

!wget --no-check-certificate https://github.com/dicodingacademy/assets/releases/download/release/rockpaperscissors.zip

# Unzip
import zipfile,os
local_zip = 'rockpaperscissors.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('rps')
zip_ref.close()

!pip install split_folders

import splitfolders

splitfolders.ratio('rps/rockpaperscissors/rps-cv-images', 'rps/rockpaperscissors/data', seed=1, ratio=(.8, .2))

base_dir = 'rps/rockpaperscissors/data'
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'val')
os.listdir('rps/rockpaperscissors/data/train')
os.listdir('rps/rockpaperscissors/data/val')

train_rock_dir = os.path.join(train_dir, 'rock')
train_scissors_dir = os.path.join(train_dir, 'scissors')
train_paper_dir = os.path.join(train_dir, 'paper')

validation_crock_dir = os.path.join(validation_dir, 'rock')
validation_scissors_dir = os.path.join(validation_dir, 'scissors')
validation_paper_dir = os.path.join(validation_dir, 'paper')

from keras.preprocessing.image import ImageDataGenerator
train_datagen = ImageDataGenerator(
  rescale=1./255, # rescale all pixel values from 0-255, so aftre this step all our pixel values are in range (0,1)
  shear_range=0.2, #to apply some random tranfromations
  zoom_range=0.2, #to apply zoom
  horizontal_flip=True) # image will be flipper horiztest_datagen = ImageDataGenerator(rescale=1./255)

test_datagen = ImageDataGenerator(
  rescale=1./255, # rescale all pixel values from 0-255, so aftre this step all our pixel values are in range (0,1)
  shear_range=0.2, #to apply some random tranfromations
  zoom_range=0.2, #to apply zoom
  horizontal_flip=True)

train_generator = train_datagen.flow_from_directory(
  train_dir, # set to the path where your ‘n’ classes of folders are present.
  target_size=(224, 224),# size of your input images, every image will be resized to this size.
  batch_size=32, # No. of images to be yielded from the generator per batch.
  color_mode='rgb', # if the image is either black and white or grayscale set “grayscale” or if the image has three color channels, set “rgb”.
  class_mode='categorical', # Set “binary” if you have only two classes to predict, if not set to“categorical”, in case if you’re developing an Autoencoder system, both input and the output would probably be the same image, for this case set to “input”
  shuffle = True, # Set True if you want to shuffle the order of the image that is being yielded, else set False
  seed=42) # Random seed for applying random image augmentation and shuffling the order of the image.
validation_generator = test_datagen.flow_from_directory(
  validation_dir,
  target_size=(224, 224),
  batch_size=32,
  color_mode='rgb',
  class_mode='categorical',
  shuffle = True,
  seed=42)

"""Visualize training & Validation images"""
sample_train_images, _ = next(train_generator)
sample_val_images, _ = next(validation_generator)

# This function will plot images in the form of a grid with 1 row and 5 columns where images are placed in each column.
def plotImages(images_arr):
    fig, axes = plt.subplots(1, 5, figsize=(20,20))
    axes = axes.flatten()
    for img, ax in zip( images_arr, axes):
        ax.imshow(img)
        ax.axis('off')
    plt.tight_layout()
    plt.show()

import matplotlib.pyplot as plt

plotImages(sample_train_images[:5])
plotImages(sample_val_images[:5])

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(224, 224, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer=tf.optimizers.Adam(),
              metrics=['accuracy'])

history = model.fit(train_generator,
          steps_per_epoch=25,
          epochs=20,
          validation_data=validation_generator,
          validation_steps=5,
          verbose=1)

#%matplotlib inline

#import matplotlib.image as mpimg
import matplotlib.pyplot as plt
# list all data in history
print(history.history.keys())
# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

import numpy as np
from keras.preprocessing import image
import matplotlib.pyplot as plt  # Import matplotlib
from google.colab import files
import os  # Import os module

uploaded = files.upload()

for fn in uploaded.keys():

  # Predict images
  path = fn
  img = image.load_img(path, target_size=(224, 224))  # Remove the third dimension (3) as it's redundant
  imgplot = plt.imshow(img)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)

  images = np.vstack([x])
  classes = model.predict(images, batch_size=32)

  print(fn)

  class_list = ['paper', 'rock', 'scissors']  # Define your class list here

  for j in range(len(class_list)):  # Use the length of class_list
    if classes[0][j] == 1.:
      print('This image belongs to class', class_list[j])
      break

model.save("mymodel.h5")