import numpy as np
import cv2
import pickle
import mysql.connector
from mysql.connector import Error

face_cascade=cv2.CascadeClassifier("C:/Users/Athira.V.Ajit/PycharmProjects/graphics/venv/Scripts/cascades/data/haarcascades/haarcascade_frontalface_default.xml")
recognizer=cv2.face.LBPHFaceRecognizer_create()
#recognizer=cv2.face.EigenFaceRecognizer_create()
recognizer.read("C:/Users/Athira.V.Ajit/PycharmProjects/graphics/venv/trainner.yml")
def connect():
    global conn
    conn = None
    try:
        conn = mysql.connector.connect(host='localhost', user='root', password='', database="embed")
    except Error as e:
        print(e)
connect()
cap=cv2.VideoCapture(0)
global conn
c=conn.cursor()
labels={"person:name"}
with open("labels.pickle",'rb') as f:
    og_labels=pickle.load(f)
    labels={v:k for k,v in og_labels.items()}

while(True):
    #Capture Frame-By-Frame
    ret, frame=cap.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray,scaleFactor=1.2,minNeighbors=5)
    for(x,y,w,h) in faces:
        #print(x,y,w,h)
        roi_gray=gray[y:y+h,x:x+w]
        roi_color=frame[y:y+h,x:x+w] #(ycord_start, ycord_end)
        roi_gray=cv2.resize(roi_gray,(500,500))
        roi_color=cv2.resize(roi_color,(500,500))
        #recognize? models
        id_,conf=recognizer.predict(roi_gray)
        #if(conf>0 and conf<30):
        #print(id_)
        print(labels[id_])
        print(conf)
        name=tuple()
        font=cv2.FONT_HERSHEY_SIMPLEX
        sql = "SELECT password FROM users WHERE id=%s"
        name=name+(str(labels[id_]),)
        k = c.execute(sql,name)
        result = c.fetchall()
        print(result)
        name=result[0]
        color=(255,255,255)
        stroke=2
        cv2.putText(frame,name,(x,y),font,1,color,stroke,cv2.LINE_AA)
        img_item="my_image.png"
        cv2.imwrite(img_item,roi_color)

        color=(255,0,0) #BGR 0-255
        stroke=2        #thickness
        end_cord_x=x+w
        end_cord_y=y+h
        cv2.rectangle(frame,(x,y),(end_cord_x,end_cord_y),color,stroke)

    #Display The Resulting Frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(20) & 0xFF ==ord('q'):
        break
def close():
    if conn is not None and conn.is_connected():
        conn.close()
        print('closed')
cap.release()
cv2.destroyAllWindows()
close()