from xml.etree.ElementInclude import include
import pandas as pd
import numpy as np 
import itertools
import tensorflow
import keras
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img 
from tensorflow.keras.models import Sequential 
from tensorflow.keras import optimizers
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import Dropout, Flatten, Dense 
from tensorflow.keras import applications 
from keras.utils.np_utils import to_categorical 
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
import math 
import datetime
import time

# Create timer decorator for 

EPOCHS = 50
BATCH_SIZE = 25

#----------------------------------------------------------------------------------------
# Working with images
#----------------------------------------------------------------------------------------
img_width, img_height = 224, 224
# Create a file to save model weights
top_model_weights_pth = 'nf_cnn_model.h5'
# Setting the dataset paths
train_dir = 'images/train'
val_dir = 'images/val'
test_dir = 'images/test'

#----------------------------------------------------------------------------------------
# Use VGG16 for Transfer Learning
#----------------------------------------------------------------------------------------
vgg16 = applications.vgg16.VGG16(include_top=False, weights='imagenet')
data_generator = ImageDataGenerator(rescale= 1. / 255) #Scales the pixels between 0 - 1

#----------------------------------------------------------------------------------------
# Create the model weights and features using VGG16
#----------------------------------------------------------------------------------------
start = datetime.datetime.now()

generator = data_generator.flow_from_directory(
    train_dir,
    target_size=(img_width, img_height),
    batch_size=BATCH_SIZE,
    class_mode=None, 
    shuffle=False
)

# Get the size of the samples
train_samples_size = len(generator.filenames)
num_classes = len(generator.class_indices)

predict_size_train = int(math.ceil(train_samples_size))
bottleneck_features_training = vgg16.predict_generator(generator, predict_size_train)




