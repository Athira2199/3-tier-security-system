from tkinter import *
import os
import mysql.connector
from mysql.connector import Error
import smtplib
import random
global name
import time
global value
global cap
value=""
count=0
name_value=""
global password
password_value=""
global conn
global email
global otp_sent
import pyttsx3
import numpy as np
import cv2
import pickle
otp_value=""
k=0
otp = str(random.randint(1000, 9999))
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file1 = os.path.join(THIS_FOLDER,'face_train.py')
my_file2 = os.path.join(THIS_FOLDER,'faces.py')
my_file3=os.path.join(THIS_FOLDER,"admin.py")
'''
INSERT OPTION FOR USER
'''
def insert(top):
    name_value=name.get()
    password_value=password.get()
    name.set("")
    password.set("")
    if(name_value=="" or password_value==""):
        engine.say("PLEASE FILL ALL FIELDS")
        engine.runAndWait()
    else:
        connect(name_value,password_value,top)

'''
INSERT OPTION AND SQL CONNECT FOR ADMIN
'''
def inserta(top,name,password):
    name_value = name.get()
    password_value = password.get()
    name.set("")
    password.set("")
    if(name_value == "" or password_value == ""):
        engine.say("PLEASE FILL ALL FIELDS")
        engine.runAndWait()
    else:
        conn=None
        try:
            conn = mysql.connector.connect(host='localhost', user='root', password='', database="embed")
            c=conn.cursor()
            name=("Admin",)
            sql = "SELECT password FROM users WHERE user=%s"
            k = c.execute(sql, name)
            result=c.fetchall()
            if (len(result) != 0):
                for x in result:
                    if (x[0] == password_value):
                        engine.say("ACCESS GRANTED")
                        engine.runAndWait()
                        os.system(my_file3)
                    else:
                        invalid(top)
            else:
                invalid(top)
        except Exception as e:
            confail(top)
            print(e)
        finally:
            if conn is not None and conn.is_connected():
                conn.close()
'''
LOGIN FOR USER
'''
def displayu(t):
    engine.say("HELLO USER")
    engine.runAndWait()
    top = Toplevel(t)
    m = Button(top, text="MUTE", fg="red", command=mute).place(x=550, y=10)
    #start=Button(t,text="START",fg="green",command=login).place(x=600,y=600)
    top.geometry("600x500")
    l=Label(top,text="LOGIN PAGE",font=(1600)).place(x=270,y=150)
    l1 = Label(top, text="NAME").place(x=230, y=200)
    name_value = Entry(top, textvariable=name).place(x=300, y=200)
    l2 = Label(top, text="PASSWORD").place(x=230, y=250)
    password_value = Entry(top, textvariable=password).place(x=300, y=250)
    s = Button(top, text="SUBMIT", fg="green", command=lambda:insert(top)).place(x=230, y=300)
    # submit.pack(side= LEFT)
    re = Button(top, text="RESET", fg="red", command=reset).place(x=300, y=300)
    # reset.pack()
    le = Button(top, text="LEAVE", fg="blue", command=lambda:destroyt(top)).place(x=370, y=300)
'''
LOGIN FOR ADMIN
'''
def displaya(t):
    engine.say("HELLO ADMIN")
    engine.runAndWait()
    top = Toplevel(t)
    #start=Button(t,text="START",fg="green",command=login).place(x=600,y=600)
    m = Button(top, text="MUTE", fg="red", command=mute).place(x=550, y=10)
    top.geometry("600x500")
    l=Label(top,text="LOGIN PAGE",font=(1600)).place(x=270,y=150)
    l1 = Label(top, text="NAME").place(x=230, y=200)
    name_value = Entry(top, textvariable=name).place(x=300, y=200)
    l2 = Label(top, text="PASSWORD").place(x=230, y=250)
    password_value = Entry(top, textvariable=password).place(x=300, y=250)
    s = Button(top, text="SUBMIT", fg="green", command=lambda:inserta(top,name,password)).place(x=230, y=300)
    # submit.pack(side= LEFT)
    re = Button(top, text="RESET", fg="red", command=reset).place(x=300, y=300)
    # reset.pack()
    le = Button(top, text="LEAVE", fg="blue", command=lambda:destroyt(top)).place(x=370, y=300)
'''
SQL CONNECT USER
'''
def connect(x,y,top):
    conn = None
    try:
        conn = mysql.connector.connect(host='localhost', user='root', password='', database="embed")
        if conn.is_connected():
            #print('Connected To MySQL database')
            c = conn.cursor()
            name = tuple()
            name = name + (x,)
            global value
            value=x
            sql = "SELECT password,email FROM users WHERE user=%s"
            k = c.execute(sql, name)
            result = c.fetchall()
            if(len(result) != 0):
                for x in result:
                    if (x[0] == y):
                        ans="WELCOME"+str(name)
                        engine.say(ans)
                        engine.runAndWait()
                        email=x[1]
                        s = sent_mail(email,top)
                        if (s == 1):
                            otp_call(top)
                            break
                    else:
                        invalid(top)
            else:
                invalid(top)
    except Exception as e:
        confail(top)
        print(e)
    finally:
        if conn is not None and conn.is_connected():
            conn.close()
'''
INVALID USER NAME PASSWORD
'''
def invalid(top):
    second = Toplevel(top)
    display = Label(second, text="INVALID USERNAME OR PASSWORD")
    engine.say("INVALID USERNAME OR PASSWORD")
    engine.runAndWait()
    display.pack()
    second.after(1000, destroy, second)
'''
OTP SENT
'''
def otp_call(top):
    first = Toplevel(t)
    first.geometry("500x500")
    top.destroy()
    m = Button(first, text="MUTE", fg="red", command=mute).place(x=450, y=10)
    display = Label(first, text="OTP HAS BEEN SENT TO MAIL")
    display.pack()
    engine.say("OTP HAS BEEN SENT TO MAIL")
    engine.runAndWait()
    display = Label(first, text="ENTER THE OTP HERE")
    display.pack()
    l3 = Label(first, text="OTP").place(x=50, y=50)
    otp_value = Entry(first, textvariable=otp_sent).place(x=120, y=50)
    submit = Button(first, text="SUBMIT", fg="green", command=lambda:otp_insert(first)).place(x=90, y=120)
    le = Button(first, text="LEAVE", fg="blue", command=leave).place(x=170, y=120)
    #first.after(5000,timeout,first)
'''
MUTE 
'''
def mute():
    global count
    count=~count
    print(count)
'''
INSERT OTP
'''
def otp_insert(first):
    otp_value=otp_sent.get()
    first.destroy()
    if(otp_value==otp):
        welcome()
    else:
        second=Toplevel(t)
        second.geometry("100x100")
        l4=Label(second,text="INVALID OTP",fg="red").place(x=50,y=50)
        engine.say("INVALID OTP")
        engine.runAndWait()
'''
DESTROY POPUPS
'''
def destroy(win):
    win.destroy()
'''
DESTROY WINDOW
'''
def destroyt(win):
    win.destroy()
    engine.say("THANK YOU")
    engine.runAndWait()
'''
TIME OUT OPTION
'''
def timeout(first):
    first.destroy()
    second = Toplevel(t)
    second.geometry("100x100")
    l4 = Label(second, text="TIME OUT", fg="red").place(x=50, y=50)
    engine.say("TIME OUT")
    engine.runAndWait()
    second.after(1000,destroy,second)
'''
LEAVE
'''
def leave():
    engine.say("THANK YOU")
    engine.runAndWait()
    exit()
'''
RESET
'''
def reset():
    name.set("")
    password.set("")
    engine.say("RESET SUCCESSFUL")
    engine.runAndWait()
'''
CONNECTION FAIL
'''
def confail(top):
    first = Toplevel(top)
    display = Label(first, text="UNABLE TO CONNECT TO DATABASE")
    engine.say("UNABLE TO CONNECT TO DATABASE")
    engine.runAndWait()
    display.pack()
    first.after(1000,destroy,first)
'''
SENT MAIL
'''
def sent_mail(email,top):
    try:
        content = 'your one time password '+otp
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login('athirava2199@gmail.com', 'athira@99')
        mail.sendmail('athirava2199@gmail.com', email , content)
        mail.quit()
        return 1
    except Exception as e:
        first = Toplevel(top)
        display = Label(first, text="UNABLE TO SENT MAIL")
        engine.say("UNABLE TO SENT MAIL")
        engine.runAndWait()
        display.pack()
        first.after(1000,destroy,first)
        print(e)
def connectf():
    global conn
    conn = None
    try:
        conn = mysql.connector.connect(host='localhost', user='root', password='', database="embed")
    except Error as e:
        print(e)
'''
START TRAINING AND RECOGNITION
'''
def welcome():
    engine.say("PLEASE WAIT")
    engine.runAndWait()
    os.system(my_file1)
    engine.say("STARTING FACE SCAN WITHIN SECONDS")
    engine.runAndWait()
    face()
def jump():
    time.sleep(5)
    global cap
    cap.release()
    cv2.destroyAllWindows()
    close()
    exit()
def close():
    if conn is not None and conn.is_connected():
        conn.close()
        print('closed')
def face():
    face_cascade=cv2.CascadeClassifier("C:/Users/Athira.V.Ajit/PycharmProjects/graphics/venv/Scripts/cascades/data/haarcascades/haarcascade_frontalface_default.xml")
    recognizer=cv2.face.LBPHFaceRecognizer_create()
    #recognizer=cv2.face.EigenFaceRecognizer_create()
    recognizer.read("C:/Users/Athira.V.Ajit/PycharmProjects/graphics/venv/trainner.yml")
    connectf()
    global cap
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
            print(value)
            if(conf>50 and conf<100 ):
                name=tuple()
                font=cv2.FONT_HERSHEY_SIMPLEX
                sql = "SELECT password FROM users WHERE id=%s"
                name=name+(str(labels[id_]),)
                k = c.execute(sql,name)
                result = c.fetchall()
                print(result)
                # import Index
                # print(Index.name)
                name=result[0][0]
                #from Index import name_value
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
                jump()
                break
                # if cv2.waitKey(20) & 0xFF ==ord('q'):
                #     jump()
                #     break
'''
INITAL PHASE
'''
if __name__=="__main__":
    engine = pyttsx3.init()
    t=Tk()
    count=0
    t.geometry("200x150")
    l=Label(t,text="WELCOME").place(x=70,y=50)
    submitu = Button(t, text="USER", fg="green", command=lambda:displayu(t)).place(x=10, y=100)
    submita = Button(t, text="ADMIN", fg="green", command=lambda:displaya(t)).place(x=70, y=100)
    le = Button(t, text="LEAVE", fg="blue", command=leave).place(x=140, y=100)
    m=Button(t,text="MUTE",fg="red",command=mute).place(x=150,y=10)
    global name
    name = StringVar()
    password = StringVar()
    otp_sent = StringVar()
    engine.say("WELCOME")
    engine.runAndWait()
    #time.sleep(5)
    t.mainloop()
