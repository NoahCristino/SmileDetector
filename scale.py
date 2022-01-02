import cv2
import numpy as np
import math

def rotate_point(center_x,center_y,angle,x,y):
  s = math.sin(angle)
  c = math.cos(angle)

  x -= center_x
  y -= center_y

  xnew = x * c - y * s;
  ynew = x * s + y * c;

  return (xnew + center_x, ynew + center_y)

def localize(points):
    d = []
    a = math.atan2(points[30][1] - points[27][1], points[30][0] - points[27][0])
    data = []
    for point in points:
        r = rotate_point(200,200,((math.pi/2)-a),point[0],point[1])
        data.append([r[0],r[1]])
    xs = [s[0] for s in data]
    ys = [s[1] for s in data]
    x_scale = abs(max(xs)-min(xs))
    y_scale = abs(max(ys)-min(ys))
    x_scaled = [(e-min(xs))/x_scale for e in xs]
    y_scaled = [(e-min(ys))/y_scale for e in ys]
    for idx, x in enumerate(x_scaled):
        d.append([x,y_scaled[idx]])
#print(x_scaled)
#print(y_scaled)
#print(max(x_scaled))
#print(max(y_scaled))
#print(xs)
display_scale = 400
frame = np.zeros((display_scale,display_scale,3), np.uint8)
for idx, x in enumerate(x_scaled):
    y = y_scaled[idx]*display_scale
    #print(x,y)
    if idx == 30 or idx == 27:
        cv2.circle(frame, (int(x*display_scale), int(y)), 1, (0, 0, 255), -1)
    else:
        cv2.circle(frame, (int(x*display_scale), int(y)), 1, (255, 0, 0), -1)
cv2.imshow("test",frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
#