import tkinter
from tkinter import *
from PIL import ImageTk, Image

from GUI import App

root = Tk()
root.geometry("530x670")
root.title('Main Menu')

smileImage = ImageTk.PhotoImage(Image.open("smile_detector_logo.png"))
smileLabel = Label(root, image=smileImage)
smileLabel.grid(row=0, column=0, columnspan=3, padx=10, pady=10)


def aboutButtonFunction(args):
    pass


aboutButton = Button(root, text = "About This Project", command=aboutButtonFunction, height=3, highlightbackground = "#586fad")
aboutButton.grid(row=1, column=0)


def creditsButtonFunction(args):
    pass


creditsButton = Button(root, text = "Credits", command=creditsButtonFunction, height =3, highlightbackground = "#586fad")
creditsButton.grid(row=1, column=1)


def smileButtonFunction():
    App(tkinter.Toplevel(), "Smile Window")


smileDetectorButton = Button(root, text = "Smile Detector", command=smileButtonFunction, height =3, highlightbackground = "#586fad")
smileDetectorButton.grid(row=1, column=2)




mainloop()










