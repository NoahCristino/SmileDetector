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


def returnHome(currWindow):
    currWindow.withdraw()
    root.deiconify()


def aboutButtonFunction():
    root.withdraw()
    aboutWindow = tkinter.Toplevel()
    aboutWindow.geometry("530x335")
    aboutWindow.title("About This Project")
    T = Text(aboutWindow, height=13, width=70, wrap=WORD, insertborderwidth=2, pady=10)
    l = Label(aboutWindow, text="About This Project")
    l.config(font=("Courier", 18))
    backButton = Button(aboutWindow, text="Return To Main Menu", command= lambda : returnHome(aboutWindow), pady=10)


    textBody = """SmileDetector is a web application that uses machine learning to detect and rate smiles. SmileDetector will calculate your ideal smile based off of your facial structure so that you can smile better in pictures. Machine learning accurately scans and maps facial vectors to your face to measure and track your facial structure and movements. After using SmileDetector you will never have to worry about posing for photos again. Soon you will be able to smile perfectly the second you see a camera."""

    T.insert(tkinter.END, textBody)
    T.config(state=DISABLED)
    l.pack()
    T.pack()
    backButton.pack()
    tkinter.mainloop()


aboutButton = Button(root, text="About This Project", command=aboutButtonFunction, height=3,
                     highlightbackground="#586fad")
aboutButton.grid(row=1, column=0)


def creditsButtonFunction():
    root.withdraw()
    creditsWindow = tkinter.Toplevel()
    creditsWindow.geometry("530x335")
    creditsWindow.title("Project Credits")
    T = Text(creditsWindow, height=13, width=70, wrap=WORD, insertborderwidth=2, pady=10)
    T.config(state=DISABLED)
    l = Label(creditsWindow, text="Project Credits")
    l.config(font=("Courier", 18))
    backButton = Button(creditsWindow, text="Return To Main Menu", command=lambda: returnHome(creditsWindow), pady=10)
    textBody = """SmileDetector is a web application that uses machine learning to detect and rate smiles. SmileDetector will calculate your ideal smile based off of your facial structure so that you can smile better in pictures. Machine learning accurately scans and maps facial vectors to your face to measure and track your facial structure and movements. After using SmileDetector you will never have to worry about posing for photos again. Soon you will be able to smile perfectly the second you see a camera."""
    T.insert(tkinter.END, textBody)
    l.pack()
    T.pack()
    backButton.pack()
    tkinter.mainloop()

creditsButton = Button(root, text="Credits", command=creditsButtonFunction, height=3, highlightbackground="#586fad")
creditsButton.grid(row=1, column=1)


def smileButtonFunction():
    App(tkinter.Toplevel(), "Smile Window")


smileDetectorButton = Button(root, text="Smile Detector", command=smileButtonFunction, height=3,
                             highlightbackground="#586fad")
smileDetectorButton.grid(row=1, column=2)

mainloop()
