import cv2
import os
import numpy as np
from PIL import Image
import sqlite3

face_cascade = cv2.CascadeClassifier("cascades/data/haarcascade_frontalface_default.xml")
video_capture = cv2.VideoCapture(0)


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('recognizer/trainingData.yml')
path = 'dataset'

def getProfile(id):
    conn=sqlite3.connect("FaceRecognition.db")
    cmd="SELECT * FROM People WHERE ID="+str(id)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile

font = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 0.6
fontcolor = (0, 155, 255)
lineType = cv2.LINE_AA

while True:
    retval, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    for(x, y, w, h) in face:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 200), 2)
        id, conf = recognizer.predict(gray[y:y+h, x:x+w])
        
        profile = getProfile(id)
        #cv2.putText(frame, "Name: " + str(profile), (x, y+h+30), font, 0.6, (0, 155, 255), lineType=cv2.LINE_AA)

        if(profile != None):
            cv2.putText(frame, "Name: " + str(profile[1]), (x, y+h+30), font, fontscale, fontcolor, 2)
            # cv2.putText(frame, str(profile[1]), (x, y+h+30), font, 1.2, (0, 155, 255), lineType=cv2.LINE_AA)
            # cv2.putText(frame, str(profile[2]), (x, y+h+60), font, 1.2, (0, 155, 255), lineType=cv2.LINE_AA)
            # cv2.putText(frame, str(profile[3]), (x, y+h+90), font, 1.2, (0, 155, 255), lineType=cv2.LINE_AA)
            # cv2.putText(frame, str(profile[4]), (x, y+h+120), font, 1.2, (0, 155, 255), lineType=cv2.LINE_AA)
    
    cv2.imshow('Face Realtime', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
video_capture.release()
cv2.destroyAllWindows()