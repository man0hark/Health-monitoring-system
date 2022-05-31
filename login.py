# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 11:37:53 2020

@author: Sowrappa
"""

import cv2
import os
import time
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
import boto3
import pandas as pd
from firebase import firebase
import shutil
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
firebase = firebase.FirebaseApplication('................', None)
s3 = boto3.resource(
    service_name='s3',
    region_name='ap-south-1',
    aws_access_key_id='..............',
    aws_secret_access_key='............'
)


def upload_photo(dir,na):
    count = 0
    for obj in s3.Bucket('login-iot').objects.all():
        count = count+1
    data =  { 'val': count+1  
             }
    result = firebase.post('/iotcount/',data)
    s3.Bucket('login-iot').upload_file(Filename=dir, Key=str(na)+'.png')


def registration(nam,my,nt):
    #yx = datetime.datetime.now()
    data =  { 
            'Name': nam,
            'Age': my,
            'Gender': nt
            }
    result = firebase.post('/named/',data)


def face_extractor(img):
    faces = face_classifier.detectMultiScale(img, 1.3, 5)
    if faces is ():
        return None
    for (x, y, w, h) in faces:
        x = x - 10
        y = y - 10
        cropped_face = img[y:y + h + 50, x:x + w + 50]
    return cropped_face


name=input("Enter name: ")
age=input("Enter age: ")
gender=input("Enter gender: ")
registration(name,age,gender)
path='test/'
try:
    os.mkdir(path)
except OSError:
        print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)
cap = cv2.VideoCapture(0)
count1 = 0
while True:
    ret, frame = cap.read()
    if face_extractor(frame) is not None:
        count1 += 1
        face = cv2.resize(face_extractor(frame), (400, 400))
        temp_name=str(count1)+'.jpg'
        file_name_path = os.path.join(path, temp_name)
        cv2.imwrite(file_name_path, face)
        cv2.putText(face, str(count1), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Face Cropper', face)
        time.sleep(0.1)
    else:
        print("Face not found")
        pass
    if cv2.waitKey(1) == 13 or count1 == 10:  # 13 is the Enter Key
        break
cap.release()
cv2.destroyAllWindows()
print("Collecting Samples Complete")
temp_file= '5.jpg'
upload_photo(os.path.join(path, temp_file),name)
shutil.rmtree(path)
