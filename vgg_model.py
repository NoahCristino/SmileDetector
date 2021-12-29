from tensorflow.keras import models
from tensorflow.keras.applications.vgg16 import VGG16
import tensorflow.keras.layers as layers
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import tensorflow.keras.utils as utils
import tensorflow as tf
import pathlib
#getting the data and splitting them into train, test, cv

import requests
requests.packages.urllib3.disable_warnings()
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context
dir = "genki"
images = list(pathlib.Path(dir).glob('*/*.jpg'))
labels = []
with open("genki/labels.txt") as f:
    for line in f:
        labels.append(int(line[0]))
# print(labels)
train = utils.image_dataset_from_directory(
    pathlib.Path(dir),
    validation_split = 0.2,
    subset = "training",
    seed = 123,
    shuffle = True,
    image_size = (224, 224),
    batch_size = 32,
    labels = labels
)

cv = utils.image_dataset_from_directory(
    pathlib.Path(dir),
    validation_split = 0.2,
    subset = "training",
    seed = 123,
    shuffle = True,
    image_size = (224, 224),
    batch_size = 32,
    labels = labels
)

model = VGG16( input_shape= (224, 224, 3), include_top = False, weights = "imagenet")
for layer in model.layers:
    layer.trainable = False

#building the last fully connected layer 
x = layers.Flatten()(model.output)
x = layers.Dense(100, activation = 'relu')(x)
x = layers.Dropout(0.3)(x)
x = layers.Dense(1, activation = 'sigmoid')(x)

final_model = Model(model.input, x)
final_model.compile(optimizer = tf.keras.optimizers.Adam(), loss = tf.keras.losses.BinaryCrossentropy(), metrics = ['accuracy'])
results = final_model.fit(train, validation_data=cv, epochs=10, steps_per_epoch=50)

