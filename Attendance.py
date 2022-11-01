import cv2
import face_recognition
import os
# from flask import Flask
from datetime import datetime, timedelta
import numpy as np

# Email Implementation

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib
from decouple import config

# app = Flask (__name__)
AttPath = "Attendance CSV"
now = datetime.now()
current_date= now.date()    
current_date_string = str(current_date)
extension =".csv"
Attendance = 'Attendance_'+ current_date_string + extension

SMTP_SERVER = config('SMTP_SERVER')
SMTP_PORT = config('SMTP_PORT')
SMTP_USERNAME = config('SMTP_USERNAME')
SMTP_PASSWORD = config('SMTP_PASSWORD')
now = datetime.now()
current_date= now.date()
EMAIL_SUBJECT = "Attendance for the Date: ",f'{current_date}'
EMAIL_FROM = config('EMAIL_FROM')
EMAIL_TO = config('EMAIL_TO')
MESSAGE_BODY= "Attendance for the Date: "+f'{current_date}'
FILE_NAME = "Attendance"
PATH_TO_CSV_FILE = f'{AttPath}/{Attendance}'

path = "ImagesAttendance"
images= []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)




# @app.route("/findEncodings")
def findEncodings(images):
    encodeList=[]
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

# if __name__ == "__main__":
#     app.run(debug=True)

AttPath = "Attendance CSV"
now = datetime.now()
current_date= now.date()
current_date_string = str(current_date)
extension =".csv"
Attendance = 'Attendance_'+ current_date_string + extension
file = open(f'{AttPath}/{Attendance}','w')
file.writelines(f'Name, Time, Date, Day, Status\n,,,,,,,,,,,,,')
file.close()

def markAttendance(name):
    with open(f'{AttPath}/{Attendance}','r+') as f:

        myDataList = f.readlines()
        nameList = []
        print(myDataList)
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])



        if name not in nameList:
            now = datetime.now()
            tString = now.strftime('%H:%M:%S')
            dString = now.date()
            dayString = now.strftime("%A")
            # dayString = now.strftime("%A %d. %B %Y")
            f.writelines(f'\n{name},{tString},{dString},{dayString}')

        time1 = datetime.now()
        day = time1.day
        month = time1.month
        year = time1.year
        time2 = datetime(year,month,day, 9,45,0)
        time3 = datetime(year,month,day, 9,0,0)
        if time1 <= time2 and time1 >= time3 and name not in nameList:
            f.writelines(f' ,On Time')
        elif name not in nameList:
            f.writelines(f' ,Late')

encodeListknown = findEncodings(images)
print("Encoding Completed")

cap = cv2.VideoCapture(1)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0), None, 0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListknown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListknown,encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name= classNames[matchIndex].upper()
            print(name)
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0), cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name)
        else:
            name= "Unknown";
            print(name)
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0), cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            

    cv2.imshow('Face Recognition',img)
    cv2.waitKey(1)
# cap.release()
# cv2.destroyAllWindow()