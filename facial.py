from imutils.video import VideoStream
from imutils import face_utils
import datetime
import argparse
import imutils
import time
import dlib
import cv2
from facePoints import image_score
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("t.dat")
vs = VideoStream().start()
time.sleep(2.0)
while True:
	# grab the frame from the threaded video stream, resize it to
	# have a maximum width of 400 pixels, and convert it to
	# grayscale
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    shape = image_score(frame)
    print(np.shape(shape))
    if shape != None:
        for idx, (x, y) in enumerate(shape):
            if idx in range(48,68):
                #color points in mouth red
                cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
            else:
                #color points in face blue
                pass #cv2.circle(frame, (x, y), 1, (255, 0, 0), -1)			
	  
	# show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if len(shape) != 0:
        cv2.waitKey(0) #breakpoint
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()