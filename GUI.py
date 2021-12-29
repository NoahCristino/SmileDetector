import os
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
from pygame import mixer

mixer.init()


class App:

    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)

        self.video_source = video_source

        # Opens computer webcam if possible
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit with the video source
        self.canvas = tkinter.Canvas(window, width=self.vid.width, height=self.vid.height)

        self.canvas.pack()

        self.btn_snapshot = tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        self.delay = 15

        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Captures a frame from the video capture
        mixer.music.load("mixkit-camera-shutter-hard-click-1430.ogg")
        mixer.music.play()
        # The commented code below was an attempt to add a white flash when the image is taken
        # img = tkinter.PhotoImage(file="white_flash.ppm")
        # self.canvas.create_image(0, 0, anchor=tkinter.NW, image=img)
        ret, frame = self.vid.get_frame()

        # The commented code below was an attempt to have the program write the images to a folder
        # called "Photos" in the directory
        # path = "/Photos"
        def display(image_name):
            root = tkinter.Tk()
            # root.title("display image")
            im = PIL.Image.open(image_name)  # This is the correct location and spelling for my image location
            photo = PIL.ImageTk.PhotoImage(im)
            cv = tkinter.Canvas()
            cv.pack()
            cv.create_image(0, 0, image=photo, anchor=None)
            root.mainloop()

        if ret:
            # cv2.imwrite(os.path.join(path, "frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg")
            #                         ,cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            image_name = "frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg"
            cv2.imwrite(image_name,
                        cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            display(image_name=image_name)

    # Returns the frame from the video source
    def update(self):
        ret, frame = self.vid.get_frame()
        if ret:
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
        else:
            return (ret, None)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


App(tkinter.Tk(), "Smile Window")
