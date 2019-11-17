import cv2
import sqlite3


def run_face():
    # Load face recognizer
    face_cascade = cv2.CascadeClassifier("cascades/data/haarcascade_frontalface_default.xml")
    video_capture = cv2.VideoCapture(0)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('recognizer/trained_model.yml')
    # path = 'datafile'

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
