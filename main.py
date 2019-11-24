# import training
# import dataset
# import facerecognition
import cv2
import os
import time
import sys
import numpy as np
from PIL import Image
import sqlite3


def run_training():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path = 'dataset'

    def get_image_with_id(path_img):
        # image_paths = [os.path.join(path_img, f) for f in os.listdir(path_img)]
        image_paths = [os.path.join(path_img, f) for f in os.listdir(path)]
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


def run_data():
    face_cascade = cv2.CascadeClassifier("cascades/data/haarcascade_frontalface_default.xml")
    video_capture = cv2.VideoCapture(0)

    def insert_or_update(ids, names, class_names, ages, genders):
        conn = sqlite3.connect("FaceRecognition.db")
        cursor = conn.execute("SELECT * FROM People WHERE ID=" + str(ids))
        is_record_exit = 0
        for _ in cursor:
            is_record_exit = 1
        if is_record_exit == 1:
            cmd = "UPDATE people SET Name=' " + str(names) + " ' WHERE ID=" + str(ids)
        else:
            cmd = "INSERT INTO people(ID,Name,Class,Age,Gender) Values(" + str(ids) + ",' " + str(
                names) + " ' , ' " + str(class_names) + " ', " + str(ages) + ", ' " + str(genders) + " ')"
        conn.execute(cmd)
        conn.commit()
        conn.close()

    print("\n [INFO] Please enter information here... \n")
    idp = input('\tEnter your id >> ')
    name = input('\tEnter your name >> ').upper()
    class_name = input('\tEnter your class >> ').upper()
    age = input('\tEnter your age >> ')
    gender = input('\tEnter your gender >> ').upper()
    insert_or_update(idp, name, class_name, age, gender)
    sample_number = 0

    print('\n [INFO] Initializing face capture. Look the camera and wait ...')

    while True:
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

        for (x, y, w, h) in face:
            sample_number = sample_number + 1
            roi_gray = gray[y:y + h, x:x + w]
            cv2.imwrite("dataset/User." + str(idp) + "." + str(sample_number) + ".jpg", roi_gray)

            color = (50, 50, 200)
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
            cv2.waitKey(100)

            cv2.imshow('FACE RECORDER', frame)

        if cv2.waitKey(1):
            if sample_number > 59:
                break

    print("\n [INFO] Exiting Program and cleanup stuff \n")
    video_capture.release()
    cv2.destroyAllWindows()


def run_face():
    # Load face recognizer
    face_cascade = cv2.CascadeClassifier("cascades/data/haarcascade_frontalface_default.xml")
    video_capture = cv2.VideoCapture(0)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('recognizer/trained_model.yml')
    # path = 'dataset'

    # Get data from FaceRecognition.db
    def get_profile(ids):
        conn = sqlite3.connect("FaceRecognition.db")
        # cmd="SELECT * FROM People WHERE ID=" + str(id)
        cursor = conn.execute("SELECT * FROM People WHERE ID=" + str(ids))
        profiles = None
        for row in cursor:
            profiles = row
        conn.close()
        return profiles

    def make_720p():
        video_capture.set(3, 960)
        video_capture.set(4, 540)

    make_720p()

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_color = (0, 155, 255)
    # line_type: int = cv2.LINE_AA

    print("\n [INFO] Camera is opening...")

    while True:
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = face_cascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in face:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 200), 2)
            id_img, conf = recognizer.predict(gray[y:y + h, x:x + w])

            profile = get_profile(id_img)

            if profile is not None:
                cv2.putText(frame, "ID: " + str(profile[0]), (x, y - 30), font, font_scale, font_color,
                            lineType=cv2.LINE_AA)
                cv2.putText(frame, "NAME: " + str(profile[1]), (x, y - 10), font, font_scale, font_color,
                            lineType=cv2.LINE_AA)
            else:
                cv2.putText(frame, "Empty!!!", (x, y - 10), font, font_scale, font_color, lineType=cv2.LINE_AA)
                # conf = "  {0}%".format(round(100 + conf))
        cv2.imshow('FACE RECORDER - Press Q to exit', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("\n [INFO] Exiting Program and cleanup stuff \n")
    video_capture.release()
    cv2.destroyAllWindows()


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def menu():
    print("\t=================== MENU ===================")
    # time.sleep(1)
    choice = input("""
        |      C: Register face.
        |      T: Training data.
        |      F: Run Camera.
        |      Q: Quit program.
        |               
        |      [Enter your choice] >> """)

    if choice == "C" or choice == "c":
        cls()
        run_data()
        menu()
    elif choice == "T" or choice == "t":
        cls()
        run_training()
        menu()
    elif choice == "F" or choice == "f":
        cls()
        run_face()
        menu()

    elif choice == "Q" or choice == "q":
        cls()
        print("\n[INFO] Exit now...")
        time.sleep(1)
        sys.exit(0)
    else:
        cls()
        print("\n\t[INFO] You must only select either C, T, F or Q.")
        print("\t[INFO] Please try again...\n")
        menu()


# main program here
if __name__ == "__main__":
    menu()
