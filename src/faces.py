import cv2
import sys
import os
import numpy as np

face_cascade = cv2.CascadeClassifier("./cascades/data/haarcascade_frontalface_default.xml")
video_capture = cv2.VideoCapture(0)

def make_720p():
    video_capture.set(3, 960)
    video_capture.set(4, 540)

make_720p()

rec = cv2.face.LBPHFaceRecognizer_create()
rec.read("./recognizer/trainingData.yml")
id = 0
font = cv2.FONT_HERSHEY_SIMPLEX
while True:
    retval, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    for(x, y, w, h) in face:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 200), 2)
        id, conf = rec.predict(gray[y:y+h, x:x+w])
        cv2.putText(frame, str(id), (x, y), font, 1.2, (0, 155, 255), lineType=cv2.LINE_AA)
    
    cv2.imshow('Face Realtime', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()