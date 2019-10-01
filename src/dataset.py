import cv2
import sqlite3

face_cascade = cv2.CascadeClassifier("./src/cascades/data/haarcascade_frontalface_default.xml")
video_capture = cv2.VideoCapture(0)

def insertOrUpdate(Id, Name):
    conn = sqlite3.connect("./src/DataFaces.db")
    #cmd="SELECT * FROM People WHERE ID=" + str(Id)
    cursor = conn.execute("SELECT * FROM People WHERE ID=" + str(Id))
    isRecordExit = 0
    for row in cursor:
        isRecordExit = 1
    if(isRecordExit == 1):
        cmd="UPDATE people SET Name=' "+str(name)+" ' WHERE ID="+str(Id)
    else:
        cmd="INSERT INTO people(ID,Name) Values("+str(Id)+",' "+str(name)+" ' )"
    conn.execute(cmd)
    conn.commit()
    conn.close()


id = input('Enter your id: ')
name = input('Enter your name: ')
insertOrUpdate(id, name)
sampleNumber = 0

while True:
    retval, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    
    for(x, y, w, h) in face:
        sampleNumber = sampleNumber+1
        roi_gray = gray[y:y+h, x:x+w]
        cv2.imwrite("src/dataset/User."+str(id)+"."+str(sampleNumber)+".jpg", roi_gray)

        color = (50, 50, 200)
        stroke = 2
        end_cord_x = x + w
        end_cord_y = y + h
        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
        cv2.waitKey(100)
    
    cv2.imshow('Face Realtime', frame)

    if cv2.waitKey(1):
        if(sampleNumber > 29):
            break

video_capture.release()
cv2.destroyAllWindows()