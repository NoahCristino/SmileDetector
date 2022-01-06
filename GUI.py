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


class App:

    def __init__(self, window, window_title, video_source=0):
        self.window = PanedWindow(window)

        self.video_source = video_source

        # Opens computer webcam if possible
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit with the video source
        self.canvas = tkinter.Canvas(window, width=self.vid.width, height=self.vid.height)

        self.canvas.grid(row=0, rowspan=3, column=0)

        # self.btn_snapshot = tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        # self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        smalllogo = Image.open("smile_detector_logo.png")
        smileimage = ImageTk.PhotoImage(smalllogo.resize((200, 200)))
        smilelabel = Label(window, image=smileimage)
        smilelabel.grid(row=0, column=1)
        
        self.is_smiling = StringVar()
        self.is_smiling.set("Status: Face not Deteced")

        statuslabel = Label(window, textvariable=self.is_smiling)
        statuslabel.grid(row=1, column=1)

        self.btn_check = Checkbutton(window, text="Show Vector Points", command=self.show_vector_points)
        self.btn_check.grid(row=2, column=1)

        self.delay = 15

        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Captures a frame from the video capture
        # mixer.music.load("mixkit-camera-shutter-hard-click-1430.ogg")
        # mixer.music.play()
        # The commented code below was an attempt to add a white flash when the image is taken
        # img = tkinter.PhotoImage(file="white_flash.ppm")
        # self.canvas.create_image(0, 0, anchor=tkinter.NW, image=img)
        ret, frame = self.vid.get_frame()

        # The commented code below was an attempt to have the program write the images to a folder
        # called "Photos" in the directory
        # path = "/Photos"
        if ret:
            # cv2.imwrite(os.path.join(path, "frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg")
            #                         ,cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            image_name = "frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg"
            cv2.imwrite(image_name,
                        cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def show_vector_points(self):
        # Shows the vector points on the mouth of the video feed
        print("hello there")

    # Returns the frame from the video source
    def update(self):
        ret, frame = self.vid.get_frame()
        if ret:

            frame = imutils.resize(frame, width=400)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            shape = image_score(frame)
            if np.ndim(shape) != 0:
                font = cv2.FONT_HERSHEY_SIMPLEX
                self.is_smiling.set("Status: Not Smiling")
                green = 0
                red = 255
                if predict(frame):
                    self.is_smiling.set("Status: Smiling")
                    green = 255
                    red = 0
                #cv2.putText(frame, t, (10,50), font, 1, (red, green, 0), 2, cv2.LINE_AA)
                for idx, (x, y) in enumerate(shape):
                    if idx in range(48,68):
                        #color points in mouth red
                        cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
                    else:
                        #color points in face blue
                        pass #cv2.circle(frame, (x, y), 1, (255, 0, 0), -1)
            else:
                self.is_smiling.set("Status: Face not Detected")
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        self.window.after(self.delay, self.update)


class MyVideoCapture:

    def __init__(self, video_source=0):

        self.vid = cv2.VideoCapture(video_source)

        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


class MainMenu:

    def __init__(self):
        self.root = Tk()
        self.root.geometry("530x670")
        self.root.title('Main Menu')
        smileImage = ImageTk.PhotoImage(Image.open("smile_detector_logo.png"))
        smileLabel = Label(self.root, image=smileImage)
        smileLabel.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        aboutButton = Button(self.root, text="About This Project", command=self.aboutButtonFunction, height=3,
                             highlightbackground="#586fad")
        aboutButton.grid(row=1, column=0)
        creditsButton = Button(self.root, text="Credits", command=self.creditsButtonFunction, height=3,
                               highlightbackground="#586fad")
        creditsButton.grid(row=1, column=1)
        smileDetectorButton = Button(self.root, text="Smile Detector", command=self.smileButtonFunction, height=3,
                                     highlightbackground="#586fad")
        smileDetectorButton.grid(row=1, column=2)
        mainloop()

    def returnHome(self, currWindow):
        currWindow.withdraw()
        self.root.deiconify()

    def aboutButtonFunction(self):
        self.root.withdraw()
        aboutWindow = tkinter.Toplevel()
        aboutWindow.geometry("530x335")
        aboutWindow.title("About This Project")
        T = Text(aboutWindow, height=13, width=70, wrap=WORD, insertborderwidth=2, pady=10)
        l = Label(aboutWindow, text="About This Project")
        l.config(font=("Courier", 18))
        backButton = Button(aboutWindow, text="Return To Main Menu", command=lambda: self.returnHome(aboutWindow),
                            pady=10)
        textBody = """SmileDetector is a web application that uses machine learning to detect and rate smiles. SmileDetector will calculate your ideal smile based off of your facial structure so that you can smile better in pictures. Machine learning accurately scans and maps facial vectors to your face to measure and track your facial structure and movements. After using SmileDetector you will never have to worry about posing for photos again. Soon you will be able to smile perfectly the second you see a camera."""
        T.insert(tkinter.END, textBody)
        T.config(state=DISABLED)
        l.pack()
        T.pack()
        backButton.pack()
        tkinter.mainloop()

    def creditsButtonFunction(self):
        self.root.withdraw()
        creditsWindow = tkinter.Toplevel()
        creditsWindow.geometry("530x335")
        creditsWindow.title("Project Credits")
        T = Text(creditsWindow, height=13, width=70, wrap=WORD, insertborderwidth=2, pady=10)
        T.config(state=DISABLED)
        l = Label(creditsWindow, text="Project Credits")
        l.config(font=("Courier", 18))
        backButton = Button(creditsWindow, text="Return To Main Menu", command=lambda: self.returnHome(creditsWindow),
                            pady=10)
        textBody = """SmileDetector is a web application that uses machine learning to detect and rate smiles. SmileDetector will calculate your ideal smile based off of your facial structure so that you can smile better in pictures. Machine learning accurately scans and maps facial vectors to your face to measure and track your facial structure and movements. After using SmileDetector you will never have to worry about posing for photos again. Soon you will be able to smile perfectly the second you see a camera."""
        T.insert(tkinter.END, textBody)
        l.pack()
        T.pack()
        backButton.pack()
        tkinter.mainloop()

    def smileButtonFunction(self):
        App(tkinter.Toplevel(), "Smile Window")


if __name__ == '__main__':
    MainMenu()
