import cv2,io,base64
from PIL import Image
import threading
from time import sleep
from imutils.video import WebcamVideoStream
import numpy as np
import cv2
#import PIL.Image
import time
#from pygame import mixer
#from tkinker import *
#from PIL import ImageTk, Image
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


class VideoCamera(object):
    def __init__(self):
        self.smiling = False
        self.history = [0,0,0,0,0,0,0,0,0,0]
        self.vid = cv2.VideoCapture(0)
        self.show_vector = True
        #added above
        self.to_process = []
        self.output_image_rgb = []
        self.output_image_bgr = []
        thread = threading.Thread(target=self.keep_processing, args=())
        thread.daemon = True
        thread.start()

    def process_one(self):
        if not self.to_process:
            return
        input_str = self.to_process.pop(0)
        imgdata = base64.b64decode(input_str)
        input_img = np.array(Image.open(io.BytesIO(imgdata)))
        """
        After getting the image you can do any preprocessing here
        """
        #_______________________________________Performing some pre processing_______________________________________________

        bgr_image = cv2.flip(input_img, 1)  # Flip the image
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB) # Changing color from bgr to rgb


        #______________________________________________________________________________________________________________________

        ret,rgb_jpeg = cv2.imencode('.jpg',rgb_image)
        _,bgr_jpeg = cv2.imencode('.jpg',bgr_image)

        self.output_image_rgb.append(self.process_frame(rgb_jpeg))
        self.output_image_bgr.append(self.process_frame(bgr_jpeg))
    
    def keep_processing(self):
        while True:
            self.process_one()
            sleep(0.01)
        
    def enqueue_input(self, input):
        self.to_process.append(input)
    
    def get_frame(self):
        while not self.output_image_rgb:
            sleep(0.05)
        return self.output_image_rgb.pop(0) , self.output_image_bgr.pop(0)
    

    def gen_panel(self,h,w):
        frame = np.zeros((h, w, 3), np.uint8)
        pts = []
        for idx, x_val in enumerate(self.history):
            p1 = int(300/(idx+1))
            p2 = int(30+(30*(1-x_val)))
            pts.append((p1,p2))
        lines = []
        for idx, pt in enumerate(pts):
            if idx+1 <= len(pts)-1:
                lines.append([pts[idx],pts[idx+1]])
        #cv2.circle(frame, (p1,p2), 1, (0, 0, 255),-1)
        for line in lines:
            cv2.line(frame, (line[0][0], line[0][1]), (line[1][0], line[1][1]), (0, 255, 0), 2)
        return  frame

    def process_frame(self, frame):
        frame = imutils.resize(frame, width=400)
        shape = image_score(frame)
        smiling = False
        if np.ndim(shape) != 0:
            # self.is_smiling.set("Status: Not Smiling")
            if predict(frame):
                # self.is_smiling.set("Status: Smiling")
                smiling = True
            self.smiling = smiling
            sh = self.history
            sh.pop(len(sh)-1)
            sh = [int(smiling)] + sh
            self.history = sh
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

        #frame design goes here
        h, w, c = frame.shape
        background = np.zeros((200, w, 3), np.uint8)
        panel = self.gen_panel(h+200, 640-w)
        frame = cv2.vconcat([frame, background])
        frame = cv2.hconcat([frame, panel])
        #end frame design 

        ret, jpeg = cv2.imencode('.jpg', cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        return jpeg.tobytes()


    def show_vector_points(self):
        # Shows the vector points on the mouth of the video feed
        self.show_vector = not self.show_vector
    


"""
# def stringToImage(base64_string):
#     imgdata = base64.b64decode(base64_string)
#     return np.array(Image.open(io.BytesIO(imgdata)))
"""