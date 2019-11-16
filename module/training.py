import cv2
import os
import numpy as np
from PIL import Image


def run_training():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path = 'images'

    def get_image_with_id(path):
        image_paths = [os.path.join(path, f) for f in os.listdir(path)]
        face_s = []
        id_s = []
        for imagePath in image_paths:
            face_img = Image.open(imagePath).convert('L')
            face_np = np.array(face_img, 'uint8')
            id_img = int(os.path.split(imagePath)[-1].split('.')[1])
            face_s.append(face_np)
            id_s.append(id_img)
            cv2.imshow("TRAINED MODEL", face_np)
            cv2.waitKey(10)
        return id_s, face_s

    print("\n [INFO] Training faces. It will take a few seconds. Wait ...")
    ids, faces = get_image_with_id(path)
    recognizer.train(faces, np.array(ids))
    recognizer.save('recognizer/trained_model.yml')

    print("\n [INFO] {0} faces trained. Exiting Program \n".format(len(np.unique(ids))))
    cv2.destroyAllWindows()
