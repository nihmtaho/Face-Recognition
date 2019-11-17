import cv2
import sqlite3


# import mysql.connector

# connSql = mysql.connector.connect(host="localhost", database="face_data_information")

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
            cv2.imwrite("datafile/User." + str(idp) + "." + str(sample_number) + ".jpg", roi_gray)

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
