from facePoints import image_score
from facePoints import localize
import cv2
import pandas as pd
from tqdm import tqdm

names = open("genki/images.txt", "r")
labels = open("genki/labels.txt", "r")
l = labels.readlines()
n = names.readlines()
df = pd.DataFrame(columns=('filename', 'smile', 'vertex_array'))
for idx, i in tqdm(enumerate(range(len(n)))):
    name = "genki/files/"+n[i].strip()
    f = cv2.imread(name)
    #print(name)
    #cv2.imshow("name",f)
    #cv2.waitKey(0)
    #break
    vertex = image_score(f)
    if vertex is None:
        continue
    vertex = localize(vertex)
    smile = l[i].strip()[0] #0 = neutral, 1 = smile
    df.loc[idx] = [name, smile, vertex]

names.close()
labels.close()
print(df.shape)
df.to_pickle("data.pkl")

#USE SVM