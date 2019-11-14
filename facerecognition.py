import cv2
import os
import numpy as np
import sqlite3

def run_face():
    #Load face recognizer
    face_cascade = cv2.CascadeClassifier("cascades/data/haarcascade_frontalface_default.xml")
    video_capture = cv2.VideoCapture(0)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('recognizer/trained_model.yml')
    path = 'images'

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

    def menu():
        print("------------------ MENU -------------------\n")
        print("\t1. Run camera. \n" + "\t2. Import infomation. \n" + "\t3. Traning \n" + "\t0. Exit program")
        print("-------------------------------------------\n")

    def main():
        chose = input('Enter your model >>')
        


    make_720p()

    font = cv2.FONT_HERSHEY_SIMPLEX
    fontscale = 0.5
    fontcolor = (0, 155, 255)
    lineType = cv2.LINE_AA

    print("\n [INFO] Camera is opening...")

    while True:
        retval, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = face_cascade.detectMultiScale(gray, 1.2, 5)
            
        for(x, y, w, h) in face:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 200), 2)
            id, conf = recognizer.predict(gray[y:y+h, x:x+w])
                
            profile = getProfile(id)

            if(profile != None):
                cv2.putText(frame, "ID: " + str(profile[0]), (x, y-30), font, fontscale, fontcolor, lineType=cv2.LINE_AA)
                cv2.putText(frame, "NAME: " + str(profile[1]), (x, y-10), font, fontscale, fontcolor, lineType=cv2.LINE_AA)
            else:
                cv2.putText(frame, "Opps!!!", (x, y-10), font, fontscale, fontcolor, lineType=cv2.LINE_AA)
                # conf = "  {0}%".format(round(100 + conf))
        cv2.imshow('FACE RECORDER - Press Q to exit', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    print("\n [INFO] Exiting Program and cleanup stuff \n")
    video_capture.release()
    cv2.destroyAllWindows()