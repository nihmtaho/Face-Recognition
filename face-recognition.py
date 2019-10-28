import cv2
import os
import numpy as np
import sqlite3

#Load face recognizer
face_cascade = cv2.CascadeClassifier("cascades/data/haarcascade_frontalface_default.xml")
video_capture = cv2.VideoCapture(0)

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('recognizer/trained_model.yml')
path = 'dataset'

# Get data from FaceRecognition.db
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


if __name__ == '__main__':
    make_720p()

    font = cv2.FONT_HERSHEY_SIMPLEX
    fontscale = 0.6
    fontcolor = (0, 155, 255)
    lineType = cv2.LINE_AA

    print("Opening camera...")

    while True:
        retval, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = face_cascade.detectMultiScale(gray, 1.2, 5)
        
        for(x, y, w, h) in face:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 200), 2)
            id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            
            profile = getProfile(id)

            if(profile != None):
                cv2.putText(frame, "ID: " + str(profile[0]), (x, y+h+20), font, fontscale, fontcolor, lineType=cv2.LINE_AA)
                cv2.putText(frame, "NAME: " + str(profile[1]), (x, y+h+40), font, fontscale, fontcolor, lineType=cv2.LINE_AA)
                cv2.putText(frame, "AGE: " + str(profile[2]), (x, y+h+60), font, fontscale, fontcolor, lineType=cv2.LINE_AA)
                cv2.putText(frame, "CLASS: " + str(profile[3]), (x, y+h+80), font, fontscale, fontcolor, lineType=cv2.LINE_AA)
                cv2.putText(frame, "GENDER: " + str(profile[4]), (x, y+h+100), font, fontscale, fontcolor, lineType=cv2.LINE_AA)
            else:
                cv2.putText(frame, "Opps!!!", (x, y+h+100), font, fontscale, fontcolor, lineType=cv2.LINE_AA)
        cv2.imshow('FACE RECORDER - Press Q to exit', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    video_capture.release()
    cv2.destroyAllWindows()