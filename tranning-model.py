import cv2
import os
import numpy as np
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()
path = 'dataset'

def getImageWithID(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    IDs = []
    for imagePath in imagePaths:
        faceImg = Image.open(imagePath).convert('L')
        faceNp = np.array(faceImg, 'uint8')
        ID = int (os.path.split(imagePath)[-1].split('.')[1])
        faces.append(faceNp)
        IDs.append(ID)
        cv2.imshow("TRAINED MODEL", faceNp)
        cv2.waitKey(10)
    return IDs, faces

print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
Ids, faces = getImageWithID(path)
recognizer.train(faces, np.array(Ids))
recognizer.save('recognizer/trained_model.yml')

print("\n [INFO] {0} faces trained. Exiting Program \n".format(len(np.unique(Ids))))
cv2.destroyAllWindows()