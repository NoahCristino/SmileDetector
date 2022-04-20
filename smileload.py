import pandas as pd
from ast import literal_eval
import cv2
import numpy as np
import imutils
from pandas import read_csv
from sklearn import svm
import random
import pickle
from facePoints import image_score
from facePoints import localize
import sys
import joblib

clf = joblib.load('model.pkl')
f = cv2.imread(sys.argv[1])
vertex = localize(image_score(f))
v_in = np.asarray([j for sub in vertex for j in sub], dtype=np.float32)
import timeit

start_time = timeit.default_timer()
prediction = clf.predict([v_in])
if int(prediction[0]) == 1:
    print("smile")
else:
    print("no smile")
print(timeit.default_timer() - start_time)
