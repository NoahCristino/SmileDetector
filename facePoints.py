from imutils.video import VideoStream
from imutils import face_utils
import datetime
import argparse
import imutils
import time
import dlib
import cv2
import sys
import cv2
import numpy as np
import math
import joblib

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("t.dat")

def image_score(frame):
    """Input: ImagePath, Output: NpArray with verticies
    """
    #frame = cv2.imread(image_path)
    frame = imutils.resize(frame, width=400)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # detect faces in the grayscale frame
    rects = detector(gray, 0)
    # loop over the face detections
    for rect in rects:
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        return shape

# This below mehtod will draw all those points which are from 0 to 67 on face one by one.
def drawPoints(image, faceLandmarks, startpoint, endpoint, isClosed=False):
  points = []
  for i in range(startpoint, endpoint+1):
    point = [faceLandmarks.part(i).x, faceLandmarks.part(i).y]
    points.append(point)

  points = np.array(points, dtype=np.int32)
  cv2.polylines(image, [points], isClosed, (255, 200, 0), thickness=2, lineType=cv2.LINE_8)

# Use this function for 70-points facial landmark detector model
# we are checking if points are exactly equal to 68, then we draw all those points on face one by one
def facePoints(image, faceLandmarks):
    assert(faceLandmarks.num_parts == 68)
    drawPoints(image, faceLandmarks, 0, 16)           # Jaw line
    drawPoints(image, faceLandmarks, 17, 21)          # Left eyebrow
    drawPoints(image, faceLandmarks, 22, 26)          # Right eyebrow
    drawPoints(image, faceLandmarks, 27, 30)          # Nose bridge
    drawPoints(image, faceLandmarks, 30, 35, True)    # Lower nose
    drawPoints(image, faceLandmarks, 36, 41, True)    # Left eye
    drawPoints(image, faceLandmarks, 42, 47, True)    # Right Eye
    drawPoints(image, faceLandmarks, 48, 59, True)    # Outer lip
    drawPoints(image, faceLandmarks, 60, 67, True)    # Inner lip

# Use this function for any model other than
# 70 points facial_landmark detector model
"""def facePoints2(image, faceLandmarks, color=(0, 255, 0), radius=4):
  for p in faceLandmarks.parts():
    cv2.circle(im, (p.x, p.y), radius, color, -1)
"""
def rotate_point(center_x,center_y,angle,x,y):
  s = math.sin(angle)
  c = math.cos(angle)

  x -= center_x
  y -= center_y

  xnew = x * c - y * s;
  ynew = x * s + y * c;

  return (xnew + center_x, ynew + center_y)

def localize(points):
    d = []
    a = math.atan2(points[30][1] - points[27][1], points[30][0] - points[27][0])
    data = []
    for point in points:
        r = rotate_point(200,200,((math.pi/2)-a),point[0],point[1])
        data.append([r[0],r[1]])
    xs = [s[0] for s in data]
    ys = [s[1] for s in data]
    x_scale = abs(max(xs)-min(xs))
    y_scale = abs(max(ys)-min(ys))
    x_scaled = [(e-min(xs))/x_scale for e in xs]
    y_scaled = [(e-min(ys))/y_scale for e in ys]
    for idx, x in enumerate(x_scaled):
        d.append([x,y_scaled[idx]])
    return d
    
def predict(img):
    clf = joblib.load('model.pkl')
    vertex = localize(image_score(img))
    v_in = np.asarray([j for sub in vertex for j in sub], dtype=np.float32)
    prediction = clf.predict([v_in])
    return bool(int(prediction[0]))