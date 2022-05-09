
import tensorflow as tf
from tensorflow.keras.applications import *
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPool2D
from tensorflow.keras import models
from tensorflow.keras import Sequential
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.metrics import Accuracy
import pandas as pd
from sklearn import model_selection
from tqdm import tqdm
from tensorflow.keras import optimizers
import os
import matplotlib.pyplot as plt


# Constants
EPOCHS = 200
BATCH_SIZE = 2
NUMBER_OF_CLASSES = 18 #Number of Forest players in directory
LEARNING_RATE = 0.01

# Set up directories and scaling
img_width, img_height, RGB_channels = 150, 150, 3
# Setting the dataset paths
train_dir = 'images/train'
val_dir = 'images/val'
input_shape = (img_width, img_height,3)

#---------------------------------------------------------------------------
# DATA PREP
#---------------------------------------------------------------------------

train_datagen = ImageDataGenerator(rescale=1./255,
                                   shear_range=0.2,
                                   zoom_range=0.6,
                                   horizontal_flip=True)

val_datagen = ImageDataGenerator(rescale=1./255,
                                shear_range=0.2, 
                                zoom_range=0.6,
                                horizontal_flip=True)

train_generator = train_datagen.flow_from_directory(
    train_dir, 
    target_size=(150,150),
    class_mode='categorical',
    batch_size=BATCH_SIZE
)

valid_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=(150,150),
    class_mode='categorical',
    batch_size=BATCH_SIZE
)


# #---------------------------------------------------------------------------
# # MODEL BUILDING
# #---------------------------------------------------------------------------
model = Sequential()
model.add(Conv2D(filters=48, kernel_size=3, activation='relu', input_shape=[150, 150, 3]))
model.add(MaxPool2D(pool_size=2, strides=2))
model.add(Conv2D(filters=48, kernel_size=3, activation='relu'))
model.add(MaxPool2D(pool_size=2, strides=2))
model.add(Conv2D(filters=32, kernel_size=3, activation='relu'))
model.add(MaxPool2D(pool_size=2, strides=2))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(NUMBER_OF_CLASSES, activation='softmax'))

# # View summary of the model 
model.summary()

checkpoint_path = "training_1/tf_weights_best.hdf5"
# Create a callback that saves the model's weights
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_best_only=True,
                                                 verbose=1, 
                                                 mode='max')

es_callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)

# # Compile the model for training
model.compile(loss='categorical_crossentropy',
               optimizer='adam',
               metrics=['accuracy'])

# # Create the model fit generator
train_n, val_n = len(train_generator.filenames), len(valid_generator.filenames)
history = model.fit(
    train_generator, 
    steps_per_epoch=train_n // BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=valid_generator,
    validation_steps=val_n // BATCH_SIZE,
    verbose=1,
    callbacks=[es_callback, cp_callback]
 )

# Visualise the loss
print(history.history.keys())
# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
plt.savefig('Model_Accuracy.png')
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
plt.savefig('Model_Loss.png')