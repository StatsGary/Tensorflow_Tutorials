# Recall best model checkpoint and validate with testing data
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import *
from tensorflow.keras import models
from tensorflow.keras.layers import Dense, Dropout,GlobalMaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.metrics import Accuracy
from tensorflow.keras import optimizers

NUMBER_OF_CLASSES = 18
BATCH_SIZE = 8
CP_FILE_PATH = 'training_1/tf_weights_best.hdf5'
LEARNING_RATE = 0.01

img_width, img_height, RGB_channels = 224, 224, 3
# Setting the dataset paths
test_dir = 'images/test'

# import model checkpoint
test_datagen = ImageDataGenerator(rescale=1./255)
testing_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(img_height, img_width),
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

input_shape = (img_width, img_height,3 )
conv_base = EfficientNetB6(weights="imagenet", include_top=False, input_shape=input_shape)

model = models.Sequential()
model.add(conv_base)
model.add(GlobalMaxPooling2D(name='gap'))
model.add(Dropout(rate=0.2, name='dropout_overfit'))
model.add(Dense(NUMBER_OF_CLASSES, activation='softmax', name='class_out'))
#Freeze the convolutional base
conv_base.trainable = False
model.load_weights(CP_FILE_PATH)
model.compile(
    loss='categorical_crossentropy', 
    optimizer=optimizers.RMSprop(learning_rate=LEARNING_RATE),
    metrics=[Accuracy()]
)

# Load model checkpoint 
predicted = model.predict(testing_generator)
label_prediction = np.argmax(predicted)
print(label_prediction)