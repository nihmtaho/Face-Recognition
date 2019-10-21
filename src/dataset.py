import cv2
import sqlite3

face_cascade = cv2.CascadeClassifier('cascades\data\haarcascade_frontalface_default.xml')
video_capture = cv2.VideoCapture(0)

def insertOrUpdate(Id, Name, ClassName, Age, Gender):
    conn = sqlite3.connect("FaceRecognition.db")
    cursor = conn.execute("SELECT * FROM People WHERE ID=" + str(Id))
    isRecordExit = 0
    for row in cursor:
        isRecordExit = 1
    if(isRecordExit == 1):
        cmd="UPDATE people SET Name=' "+str(name)+" ' WHERE ID="+str(Id)
    else:
        cmd="INSERT INTO people(ID,Name,Class,Age,Gender) Values("+str(Id)+",' "+str(name)+" ' , ' "+str(className)+" ', "+str(age)+", ' "+str(gender)+" ')"
    conn.execute(cmd)
    conn.commit()
    conn.close()


id = input('Enter your id: ')
name = input('Enter your name: ')
className = input('Enter your class: ')
age = input('Enter your age: ')
gender = input('Enter your gender: ')
insertOrUpdate(id, name, className, age, gender)
sampleNumber = 0

print('\nYOUR FACES ARE RECORDING... ')

while True:
    retval, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    
    for(x, y, w, h) in face:
        sampleNumber = sampleNumber+1
        roi_gray = gray[y:y+h, x:x+w]
        cv2.imwrite("dataset/User."+str(id)+"."+str(sampleNumber)+".jpg", roi_gray)

        color = (50, 50, 200)
        stroke = 2
        end_cord_x = x + w
        end_cord_y = y + h
        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
        cv2.waitKey(100)
    
    cv2.imshow('Face Realtime', frame)

    if cv2.waitKey(1):
        if(sampleNumber > 99):
            break

print('\nYOUR FACES HAS BEEN IN DATABASE... \n')

video_capture.release()
cv2.destroyAllWindows()