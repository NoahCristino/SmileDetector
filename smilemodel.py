import pandas as pd
from ast import literal_eval
import cv2
import numpy as np
import imutils
from pandas import read_csv
from sklearn import svm
import random
import joblib
from facePoints import image_score
from facePoints import localize
import sys
name = []
x = []
y = []
df = pd.read_pickle('data.pkl')
#print(df.head())
#df.vertex_array = df.vertex_array.apply(literal_eval)
for index, row in df.iterrows():
    name.append(row["filename"])
    y.append(row["smile"])
    x.append([j for sub in row["vertex_array"] for j in sub])
x = np.asarray(x, dtype=np.float32)
y = np.asarray(y, dtype=np.float32)
clf = svm.SVC()
clf.fit(x, y)
total = 0
correct = 0
for idx, inpu in enumerate(x):
    o = clf.predict([inpu])
    if o == y[idx]:
        correct+=1+
    total+=1

print("accuracy: "+str(correct/total))
joblib.dump(clf, "model.pkl")