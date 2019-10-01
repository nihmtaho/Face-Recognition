import cv2
import sys
import os
import numpy as np


face_cascade = cv2.CascadeClassifier("./cascades/data/haarcascade_frontalface_default.xml")
video_capture = cv2.VideoCapture(0)


while True:
    retval, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    for(x, y, w, h) in face:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 200), 2)
    
    cv2.imshow('Face Realtime', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        sys.exit(0)