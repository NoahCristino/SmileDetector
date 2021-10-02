from imutils.video import VideoStream
from imutils import face_utils
import datetime
import argparse
import imutils
import time
import dlib
import cv2
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
	# detect faces in the grayscale frame
	rects = detector(gray, 0)
	# loop over the face detections
	for rect in rects:
		# determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)
		# loop over the (x, y)-coordinates for the facial landmarks
		# and draw them on the image
		"""
		
		nose: points 27 to 35
		right eye: points 42 to 47
		left eye: points 36 to 41
		mouth: points 48 to 67
		left eyebrow: points 17 to 21
		right eyebrow: points 22 to 26
		contour of the face: points 0 to 16 (chin: 6 to 10)

		"""
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
	if len(rects) != 0:
		cv2.waitKey(0) #breakpoint
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()