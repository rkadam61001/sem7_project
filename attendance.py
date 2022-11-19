import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime 
import csv
import smtplib
import mysql.connector as connectionserver

from dotenv import load_dotenv
load_dotenv()


try:
    mydb = connectionserver.connect(
        host=os.getenv('host'), 
        user=os.getenv('user'), 
        password=os.getenv('password'),
        database = os.getenv('database'),
    )
except:
    print("Error occurred while connecting to database")
    exit()

if mydb.is_connected:
    print("Successfully connected to database")

mycursor = mydb.cursor()
    




path = 'imagesDatabase'
studentNames = []
images = []

imagesList = os.listdir(path)


sender_email = "rohit.jindamwar@walchandsangli.ac.in"
password = input(str("Enter your gmail password: "))

message = "Your Attendance has been Marked"

server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(sender_email,password)
print("Login successful to your gmail account")



for currentImg in imagesList :
    curImg = cv2.imread(f'{path}/{currentImg}')
    images.append(currentImg)
    studentNames.append(os.path.splitext(currentImg)[0])

students = studentNames.copy()

print(studentNames)


def findEncodings (images):
    encodingList = []
    for img in images:
        img = cv2.imread(f'{path}/{img}')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # converted to RGB 
        encode = face_recognition.face_encodings(img)[0]
        encodingList.append(encode)
    return encodingList



knownEncodingList = findEncodings(images)
print("Encoding Done")

cap =  cv2.VideoCapture(1)

now = datetime.now()
currentDate = now.strftime("%Y-%m-%d")

f = open(currentDate+'.csv','w+',newline='')
lnwriter = csv.writer(f)
faceNames = []
check = True

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while (True):
    success,frame = cap.read()

    
    # if not success:
    #     print("no frame captured")
    #     exit()

    # if(frame==None):
    #     print("no frame captured")
    #     exit()
    

    if success:
        imgS = cv2.resize(frame,(0,0),None,0.25,0.25)
    
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB) # converted to RGB

        if check:

            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

            for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):

                
                matches = face_recognition.compare_faces(knownEncodingList,encodeFace)
                faceDist = face_recognition.face_distance(knownEncodingList,encodeFace)
                
                
                matchIndex = np.argmin(faceDist)

                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),2)
                cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                if matches[matchIndex]:
                    name=studentNames[matchIndex]
                    faceNames.append(name)
                if matches[matchIndex] == False :
                    name = 'UNKNOWN'
                    
                
                cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                if name in studentNames:
                    if name in students:
                        print(name)
                        students.remove(name)
                        
                        current_time=now.strftime("%H-%M-%S")
                        lnwriter.writerow([name,current_time])
                        
                        namelist = [name]   #converting  string to list. name is string and namelist is a list
                        
                        
                        query = "SELECT Email FROM StudentInfo WHERE Name= %s"
                        mycursor.execute(query,(namelist))

                        myresult = mycursor.fetchone()
                        
                        for mail in myresult:
                            server.sendmail(sender_email,mail,message)
                            print("Email sent to ",mail)

    else:
        break
                   
    cv2.imshow("attendance sys",frame)
    if(cv2.waitKey(1)& 0xFF==ord('q')):
        break

cap.release()
cv2.destroyAllWindows()
f.close()

