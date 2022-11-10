



import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime 
import csv


path = 'imagesDatabase'
studentNames = []
images = []

imagesList = os.listdir(path)


for currentImg in imagesList :
    curImg = cv2.imread(f'{path}/{currentImg}')
    images.append(currentImg)
    studentNames.append(os.path.splitext(currentImg)[0])

students = studentNames.copy()

print(studentNames)
#print(students)

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

cap =  cv2.VideoCapture(0)

now = datetime.now()
currentDate = now.strftime("%Y-%m-%d")

f = open(currentDate+'.csv','w+',newline='')
lnwriter = csv.writer(f)
faceNames = []
check = True

while True:
    success,frame = cap.read()

    
    # if not success:
    #     print("no frame captured")
    #     exit()

    imgS = cv2.resize(frame,(0,0),None,0.25,0.25)
    # imgS = cv2.resize(img,(1280,720))
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
                    #print(students)
                    current_time=now.strftime("%H-%M-%S")
                    lnwriter.writerow([name,current_time])
                   
    cv2.imshow("attendance sys",frame)
    if(cv2.waitKey(1)& 0xFF==ord('q')):
        break

cap.release()
cv2.destroyAllWindows()
f.close()






# import cv2
# import face_recognition
# import numpy as np
# import os
# from datetime import datetime 
# import csv


# path = 'imagesDatabase'
# studentNames = []
# images = []

# imagesList = os.listdir(path)


# for currentImg in imagesList :
#     curImg = cv2.imread(f'{path}/{currentImg}')
#     images.append(currentImg)
#     studentNames.append(os.path.splitext(currentImg)[0])

# students = studentNames.copy()

# print(studentNames)

# def findEncodings (images):
#     encodingList = []
#     for img in images:
#         img = cv2.imread(f'{path}/{img}')
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # converted to RGB 
#         encode = face_recognition.face_encodings(img)[0]
#         encodingList.append(encode)
#     return encodingList



# knownEncodingList = findEncodings(images)
# print("Encoding Done")

# cap =  cv2.VideoCapture(0)

# now = datetime.now()
# currentDate = now.strftime("%Y-%m-%d")

# f = open(currentDate+'.csv','w+',newline='')
# lnwriter = csv.writer(f)
# faceNames = []
# check = True

# while True:
#     success,frame = cap.read()

    
#     # if not success:
#     #     print("no frame captured")
#     #     exit()

#     imgS = cv2.resize(frame,(0,0),None,0.25,0.25)
#     # imgS = cv2.resize(img,(1280,720))
#     imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB) # converted to RGB

#     if check:

#         facesCurFrame = face_recognition.face_locations(imgS)
#         encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

#         for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):

            
#             matches = face_recognition.compare_faces(knownEncodingList,encodeFace)

#             faceDist = face_recognition.face_distance(knownEncodingList,encodeFace)

#             matchIndex = np.argmin(faceDist)

#             y1,x2,y2,x1 = faceLoc
#             y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
#             cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
#             cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)

#             if matches[matchIndex]:
#                 name = studentNames[matchIndex].upper()
#                 faceNames.append(name)
                
            
#             if matches[matchIndex] == False :
#                 name = 'UNKNOWN'
                
            
#             cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
        
            

#             if name in studentNames :
#                 if name in students:
#                     students.remove(name)
#                     print("students: " + students)
#                     currentTime = now.strftime("%H-%M-%S")
#                     lnwriter.writerow([name,currentTime])
#     cv2.imshow('Attendence System',frame)
#     key = cv2.waitKey(1) & 0xFF
    
#     if key == ord('q'): # if the `q` key was pressed, break from the loop
#         break

# cap.release()
# cv2.destroyAllWindows()
# f.close()