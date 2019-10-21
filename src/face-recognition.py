import cv2
import numpy as np
import sqlite3

face_cascade = cv2.CascadeClassifier("cascades/data/haarcascade_frontalface_default.xml")
video_capture = cv2.VideoCapture(0)


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('recognizer/trainingData.yml')
path = 'dataset'

def getProfile(id):
    conn=sqlite3.connect("FaceRecognition.db")
    #cmd="SELECT * FROM People WHERE ID=" + str(id)
    cursor=conn.execute("SELECT * FROM People WHERE ID=" + str(id))
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile

def make_720p():
    video_capture.set(3, 960)
    video_capture.set(4, 540)

make_720p()

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

        if(profile != None):
            cv2.putText(frame, "Id: " + str(profile[0]), (x, y+h+20), font, fontscale, fontcolor, lineType=cv2.LINE_AA)
            cv2.putText(frame, "Name: " + str(profile[1]), (x, y+h+40), font, fontscale, fontcolor, lineType=cv2.LINE_AA)
            cv2.putText(frame, "Age: " + str(profile[2]), (x, y+h+60), font, fontscale, fontcolor, lineType=cv2.LINE_AA)
            cv2.putText(frame, "Class: " + str(profile[3]), (x, y+h+80), font, fontscale, fontcolor, lineType=cv2.LINE_AA)
            cv2.putText(frame, "Gender: " + str(profile[4]), (x, y+h+100), font, fontscale, fontcolor, lineType=cv2.LINE_AA)
    
    cv2.imshow('Face Realtime', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
video_capture.release()
cv2.destroyAllWindows()