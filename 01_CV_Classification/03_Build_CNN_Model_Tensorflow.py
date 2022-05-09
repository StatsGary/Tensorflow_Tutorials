
import tensorflow as tf
from tensorflow.keras.applications import *
from tensorflow.keras import models
from tensorflow.keras.layers import Dense, Dropout,GlobalMaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.metrics import Accuracy
import pandas as pd
from sklearn import model_selection
from tqdm import tqdm
from tensorflow.keras import optimizers
import os
import matplotlib.pyplot as plt

# Check if GPU is configured correctl
#Use this to check if the GPU is configured correctly
from tensorflow.python.client import device_lib
#print(device_lib.list_local_devices())

EPOCHS = 5
BATCH_SIZE = 8
NUMBER_OF_CLASSES = 18 #Number of Forest players in directory
LEARNING_RATE = 0.01

#----------------------------------------------------------------------------------------
# Working with images
#----------------------------------------------------------------------------------------
img_width, img_height, RGB_channels = 224, 224, 3
# Setting the dataset paths
train_dir = 'images/train'
val_dir = 'images/val'
test_dir = 'images/test'

#----------------------------------------------------------------------------------------
# Use EfficientNet
#----------------------------------------------------------------------------------------
input_shape = (img_width, img_height,3 )
conv_base = EfficientNetB6(weights="imagenet", include_top=False, input_shape=input_shape)

# Configure model for custom dataset
model = models.Sequential()
model.add(conv_base)
model.add(GlobalMaxPooling2D(name='gap'))
model.add(Dropout(rate=0.2, name='dropout_overfit'))
model.add(Dense(NUMBER_OF_CLASSES, activation='softmax', name='class_out'))
#Freeze the convolutional base
conv_base.trainable = False

#----------------------------------------------------------------------------------------
# Create ImageDataGenerators
#----------------------------------------------------------------------------------------
train_datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest",
)
# Do not augment your validation data
val_datagen = ImageDataGenerator(rescale=1.0 / 255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    # All images will be resized to target height and width.
    target_size=(img_height, img_width),
    batch_size=BATCH_SIZE,
    # Since we use categorical_crossentropy loss, we need categorical labels
    class_mode="categorical",
)

no_train_images = len(train_generator.filenames)

# Create validation generator
validation_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=(img_height, img_width),
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)


# Pull out the size of the train, val and test gen 
train_n, val_n = len(train_generator.filenames), len(validation_generator.filenames)
print(f'There are {train_n} examples in the train set and {val_n} in the validation set.')

model.compile(
    loss='categorical_crossentropy', 
    optimizer=optimizers.RMSprop(learning_rate=LEARNING_RATE),
    metrics=[Accuracy()]
)

print(model.summary())

checkpoint_path = "training_1/tf_weights_best.hdf5"

# Create a callback that saves the model's weights
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_best_only=True,
                                                 verbose=1, 
                                                 mode='max')

es_callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=3)
# Train the model
history = model.fit(
    train_generator, 
    steps_per_epoch=train_n // BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=validation_generator,
    validation_steps=val_n // BATCH_SIZE,
    verbose=1,
    callbacks=[es_callback, cp_callback])

# Plot the history
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

