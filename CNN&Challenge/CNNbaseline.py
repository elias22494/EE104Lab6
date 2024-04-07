# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 16:00:11 2022
## https://machinelearningmastery.com/how-to-develop-a-cnn-from-scratch-for-cifar-10-photo-classification/
@author: Christopher Pham
"""



import tensorflow as tf
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt

#import cv2
#import albumentations as A
#import random

#from matplotlib import pyplot as plt

from tensorflow import keras
#from keras import callbacks

from keras.optimizers import SGD
from keras.layers import GaussianNoise
from keras.callbacks import ReduceLROnPlateau
from keras.layers import Dropout, Dense
from keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import keras

#https://stackoverflow.com/questions/69687794/unable-to-manually-load-cifar10-dataset
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


(train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()

# Normalize pixel values to be between 0 and 1
train_images, test_images = train_images / 255.0, test_images / 255.0



## verify that the dataset looks correct
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']

plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i])
    # The CIFAR labels happen to be arrays, 
    # which is why you need the extra index
    plt.xlabel(class_names[train_labels[i][0]])
plt.show()

# define cnn BaseLine model
model = models.Sequential()

##########################################################################################################################################################
### This section is from https://colab.research.google.com/github/tensorflow/docs/blob/master/site/en/tutorials/images/cnn.ipynb#scrollTo=WRzW5xSDDbNF ###
### You will improve this section for higher accuracy 
##########################################################################################################################################################
# Create the convolutional base 3 VGG Blocks
model = models.Sequential()

model.add(layers.Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=(32, 32, 3)))
model.add(BatchNormalization())
model.add(layers.Conv2D(32, (3, 3), padding='same', activation='relu'))
model.add(BatchNormalization())

model.add(layers.MaxPooling2D((2, 2)))
model.add(Dropout(0.1))

model.add(layers.Conv2D(64, (3, 3), padding='same', activation='relu'))
model.add(BatchNormalization())
model.add(layers.Conv2D(64, (3, 3), padding='same', activation='relu'))
model.add(BatchNormalization())

model.add(layers.MaxPooling2D((2, 2)))
model.add(Dropout(0.25))

model.add(layers.Conv2D(128, (3, 3), padding='same', activation='relu'))
model.add(BatchNormalization())
model.add(layers.Conv2D(128, (3, 3), padding='same', activation='relu'))
model.add(BatchNormalization())
model.add(layers.MaxPooling2D((2, 2)))
model.add(Dropout(0.4))


# Add Dense layers on top
model.add(layers.Flatten())
model.add(layers.Dense(256, input_dim=2, activation='relu'))
model.add(Dropout(0.5))
model.add(GaussianNoise(0.5))
model.add(layers.Dense(10,  activation='softmax'))


# Here's the complete architecture of your model:
model.summary()

### End code from https://colab.research.google.com/github/tensorflow/docs/blob/master/site/en/tutorials/images/cnn.ipynb#scrollTo=WRzW5xSDDbNF ####
##########################################################################################################################################################



## Compile and train the model
datagen = ImageDataGenerator(width_shift_range=0.05, height_shift_range=0.05, horizontal_flip=True) #Data Augment
it_train = datagen.flow(train_images, train_labels, batch_size=64)
steps = int(train_images.shape[0] / 64)

opt = SGD(learning_rate=0.001, momentum=0.9)
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
callbacks_list = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.8, patience=3)#ramp down LR when loss increases

history = model.fit(train_images, train_labels, epochs=40,
                    callbacks=callbacks_list,
                    validation_data=(test_images, test_labels)
                    )



## Evaluate the model
plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0.5, 1])
plt.legend(loc='lower right')

test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)

print(test_acc)

########################################################
## save trained model in file "MyGroup_CIFARmodel.h5" ##
# You will use this trained model to test the images  ##
########################################################
model.save('MyGroup_CIFARmodel.h5')