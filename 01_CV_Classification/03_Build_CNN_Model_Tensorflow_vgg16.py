from tkinter import Image
import tensorflow as tf
from keras import layers
from keras import models
from keras import optimizers

# Constants
EPOCHS = 20
BATCH_SIZE = 2
NUMBER_OF_CLASSES = 18 #Number of Forest players in directory
LEARNING_RATE = 0.01

# Set up directories and scaling
img_width, img_height, RGB_channels = 224, 224, 3
# Setting the dataset paths
train_dir = 'images/train'
val_dir = 'images/val'
input_shape = (img_width, img_height,3)

#---------------------------------------------------------------------------
# DATA PREP
#---------------------------------------------------------------------------

from keras.preprocessing import ImageDataGenerator
train_datagen = ImageDataGenerator(rescale=1./255)
val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir, 
    target_size=(150,150),
    batch_size=20, 
    class_mode='categorical'
)

valid_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=(150,150),
    batch_size=20,
    class_mode='categorical'
)


#---------------------------------------------------------------------------
# MODEL BUILDING
#---------------------------------------------------------------------------
model = models.Sequential()
model.add(layers.Conv2D(32, (3,3), activation='relu', input_shape=(150,150,3)))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(64, (3,3), activation='relu'))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(128, (3,3), activation='relu'))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(128, (3,3), activation='relu'))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Flatten())
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(NUMBER_OF_CLASSES, activation='softmax'))

# View summary of the model 
model.summary()

# Compile the model for training
model.compile(loss='categorical_crossentropy',
              optimizer=optimizers.RMSprop(lr=LEARNING_RATE),
              metrics=['acc'])

# Create the model fit generator