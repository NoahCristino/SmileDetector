import os
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
from pygame import mixer
from tkinter import *
from PIL import ImageTk, Image
from imutils.video import VideoStream
from imutils import face_utils
import datetime
import argparse
import imutils
import dlib
import numpy as np
from facePoints import image_score
from facePoints import predict
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("t.dat")
time.sleep(2.0) #not sure if nessicary

mixer.init()

class VideoCamera:

    def __init__(self, video_source=0):

        self.vid = cv2.VideoCapture(video_source)
        self.show_vector = True
        # self.is_smiling = StringVar()
        # self.is_smiling.set("Status: Face not Deteced")

        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return self.process_frame(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return None

    def process_frame(self, frame):
        frame = imutils.resize(frame, width=400)
        shape = image_score(frame)
        smiling = False
        if np.ndim(shape) != 0:
            # self.is_smiling.set("Status: Not Smiling")
            if predict(frame):
                # self.is_smiling.set("Status: Smiling")
                smiling = True
            if self.show_vector:
                for idx, (x, y) in enumerate(shape):
                    if idx in range(48,68):
                        #color points in mouth red
                        if smiling:
                            cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
                        else:
                            cv2.circle(frame, (x, y), 1, (255, 0, 0), -1)
            # else:
                # self.is_smiling.set("Status: Face not Detected")

        ret, jpeg = cv2.imencode('.jpg', cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        return jpeg.tobytes()


    def show_vector_points(self):
        # Shows the vector points on the mouth of the video feed
        self.show_vector = not self.show_vector

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()