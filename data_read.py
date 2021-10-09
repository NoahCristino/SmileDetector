import pandas as pd
from ast import literal_eval
import cv2
import imutils

df = pd.read_pickle('data.pkl')
#df.vertex_array = df.vertex_array.apply(literal_eval)
for index, row in df.iterrows():
    frame = cv2.imread(row['filename'])
    frame = imutils.resize(frame, width=400)
    t = "No Smile Detected"
    if row['smile'] == "1":
        t = "Smile Detected"
    cv2.putText(frame, t, (40,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0))
    for idx, (x, y) in enumerate(row["vertex_array"]):
        if idx in range(48,68):
            cv2.circle(frame, (x, y), 1, (255, 0, 0), -1)
    #cv2.imshow(row['filename'],frame)
    cv2.imwrite(row['filename'],frame)
    cv2.waitKey(0)
cv2.destroyAllWindows()