from facePoints import predict
import cv2
import sys

if (len(sys.argv) == 1):
    quit("invalid parameters!")

vidcap = cv2.VideoCapture(sys.argv[1])
success,image = vidcap.read()
count = 0
smiles = 0
jump = 1
smile_locations = []
while success:
  if (predict(image)):
    smile_locations.append(count)
  print("frame " + str(count))    
  #else:
   # print("frame " + str(count)+ ": not smiling")
  for i in range(jump):
    success,image = vidcap.read()
  count += jump
print(smiles/count)
from matplotlib import pyplot as plt
import numpy as np

plt.hlines(1,1,6000)  # Draw a horizontal line
plt.xlim(0,6001)
plt.ylim(0.5,1.5)

y = np.ones(np.shape(smile_locations))   # Make all y values the same
plt.plot(smile_locations,y,'|',ms = 40)  # Plot a line at each location specified in a
plt.axis('off')
plt.show()