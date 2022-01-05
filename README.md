# SmileDetector
https://utmist.gitlab.io/projects/smiledetector/

# Files

**build_data.py** - generates pandas dataframe using images in genki folder

**facePoints.py** - library containing functions:

* predict: makes prediction with model

* localize: rotates detected points on face to ensure correct orientation and scales based on image size

* image_score: generates list of points on mouth

**facial.py** - remove and incorporate into GUI (live prediction on webcam)

**GUI.py** - runs live webcam feed with GUI

**mainMenu.py** - main menu that displays credits and calls GUI (should we merge GUI and mainMenu into 1 file?)

**smileload.py** - takes in 1 argument which is an image file to run model prediction on

**smilemodel.py** - trains model