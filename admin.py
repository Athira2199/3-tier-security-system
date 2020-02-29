from tkinter import *
import pyttsx3
import mysql.connector
from mysql.connector import Error
global conn
global count
import cv2
import os
import time
count=0
conn=None
global namevalue
global idvalue
global emailvalue
global passwordvalue
'''
CREATING ADD FUNCTION
'''
def add(t):
    top=Toplevel(t)
    top.geometry("600x500")
    l1 = Label(top, text="NAME").place(x=30, y=40)
    name_value = Entry(top, textvariable=name).place(x=100, y=40)
    re = Button(top, text="RESET", fg="red", command=lambda:reset(name)).place(x=250, y=40)
    l2 = Label(top, text="PASSWORD").place(x=30, y=80)
    password_value = Entry(top, textvariable=password).place(x=100, y=80)
    re = Button(top, text="RESET", fg="red", command=lambda:reset(password)).place(x=250, y=80)
    s = Button(top, text="SUBMIT", fg="green",).place(x=230, y=300)
    l3 = Label(top, text="EMAIL").place(x=30, y=120)
    email_value = Entry(top, textvariable=email).place(x=100, y=120)
    re = Button(top, text="RESET", fg="red", command=lambda:reset(email)).place(x=250, y=120)
    l4 = Label(top, text="ID").place(x=30, y=160)
    id_value = Entry(top, textvariable=id).place(x=100, y=160)
    re = Button(top, text="RESET", fg="red", command=lambda:reset(id)).place(x=250, y=160)
    #cd=Button(top, text="CREATE DIRECTORY", fg="blue", command=lambda:create(name)).place(x=30, y=200)
    s = Button(top, text="SUBMIT", fg="green",command=lambda: insert(name,password,email,id,top)).place(x=230, y=300)
    le = Button(top, text="LEAVE", fg="blue", command=lambda: destroy(top)).place(x=370, y=300)
    re = Button(top, text="RESET ALL", fg="red", command=lambda: resetall(name, password, email, id)).place(x=510, y=300)
'''
CREATING DELETE FUNCTION 
'''
def delete(t):
    top = Toplevel(t)
    top.geometry("300x200")
    l4 = Label(top, text="ID").place(x=30, y=60)
    id_value = Entry(top, textvariable=id).place(x=100, y=60)
    re = Button(top, text="RESET", fg="red", command=lambda:reset(id)).place(x=250, y=60)
    s = Button(top, text="SUBMIT", fg="green", command=lambda: remove(id,top)).place(x=150,y=150)
'''
CREATING UPDATE FUNCTION
'''
def update(t):
    top = Toplevel(t)
    top.geometry("600x500")
    l1 = Label(top, text="NAME").place(x=30, y=40)
    name_value = Entry(top, textvariable=name).place(x=100, y=40)
    re = Button(top, text="RESET", fg="red", command=lambda:reset(name)).place(x=250, y=40)
    l2 = Label(top, text="PASSWORD").place(x=30, y=80)
    password_value = Entry(top, textvariable=password).place(x=100, y=80)
    re = Button(top, text="RESET", fg="red", command=lambda:reset(password)).place(x=250, y=80)
    s = Button(top, text="SUBMIT", fg="green", ).place(x=230, y=300)
    l3 = Label(top, text="EMAIL").place(x=30, y=120)
    email_value = Entry(top, textvariable=email).place(x=100, y=120)
    re = Button(top, text="RESET", fg="red", command=lambda:reset(email)).place(x=250, y=120)
    l4 = Label(top, text="ID").place(x=30, y=160)
    id_value = Entry(top, textvariable=id).place(x=100, y=160)
    re = Button(top, text="RESET", fg="red", command=lambda:reset(id)).place(x=250, y=160)
    s = Button(top, text="SUBMIT", fg="green", command=lambda: renew(name, password, email, id, top)).place(x=230,y=300)
    le = Button(top, text="LEAVE", fg="blue", command=lambda: destroy(top)).place(x=370, y=300)
    re = Button(top, text="RESET ALL", fg="red", command=lambda: resetall(name,password,email,id)).place(x=510, y=300)
'''
RENEW FUNCTION
'''
def renew(name,password,email,id,top):
    n=name.get()
    p=password.get()
    e=email.get()
    i=id.get()
    cursor = conn.cursor()
    sql = "UPDATE users SET user=%s,password=%s,email=%s WHERE id=%s"
    value=(n,p,e,i)
    cursor.execute(sql, value)
    conn.commit()
    if (cursor.rowcount != 0):
        msg = "UPDATED ID NUMBER " + i
        engine.say(msg)
        engine.runAndWait()
    else:
        engine.say("NO UPDATE POSSIBLE")
        engine.runAndWait()
'''
REMOVE FROM DATABASE
'''
def remove(id,top):
    cursor = conn.cursor()
    idv=id.get()
    value=tuple()
    value = value+(idv, )
    sql = "DELETE FROM users WHERE id=%s"
    cursor.execute(sql, value)
    conn.commit()
    if (cursor.rowcount != 0):
        msg="DELETED ID NUMBER "+idv
        engine.say(msg)
        engine.runAndWait()
    else:
        engine.say("NO SUCH ID")
        engine.runAndWait()
'''
LEAVE
'''
def destroy(top):
    top.destroy()
    engine.say("THANK YOU")
    engine.runAndWait()
'''
RESET
'''
def reset(k):
    k.set("")
    engine.say("RESET SUCCESSFUL")
    engine.runAndWait()
def resetall(a,b,c,d):
    a.set("")
    b.set("")
    c.set("")
    d.set("")
    engine.say("RESET SUCCESSFUL")
    engine.runAndWait()
'''
CONNECT TO DATABASE
'''
def connect():
    global conn
    conn=None
    try:
        conn=mysql.connector.connect(host='localhost',user='root',password='',database="embed")
    except Error as e:
        print(e)
'''
INSERT INTO DATABASE
'''
def insert(name,password,email,id,top):
    global conn
    global namevalue
    global idvalue
    global emailvalue
    global passwordvalue
    namevalue = name.get()
    passwordvalue = password.get()
    emailvalue=email.get()
    idvalue=id.get()
    name.set("")
    password.set("")
    email.set("")
    id.set("")
    if conn is not None and conn.is_connected():
        if (namevalue == "" or passwordvalue == "" or emailvalue=="" or idvalue==""):
            engine.say("PLEASE FILL ALL FIELDS")
            engine.runAndWait()
        else:
            create(idvalue,top)
                # msg="ADDED"+namevalue
                # engine.say(msg)
                # engine.runAndWait()
    else:
        confail(top)
'''
CLOSE CONNECTION
'''
def close():
    if conn is not None and conn.is_connected():
        conn.close()
        print('closed')
'''
CONNECTION FAIL MESSAGE
'''
def confail(top):
    first = Toplevel(top)
    display = Label(first, text="UNABLE TO CONNECT TO DATABASE")
    engine.say("UNABLE TO CONNECT TO DATABASE")
    engine.runAndWait()
    display.pack()
    first.after(1000,destroy,first)
def addimage(top,path):
    t=Toplevel(top)
    t.geometry("500x500")
    t.overrideredirect("True")
    global count
    msg = "NO OF IMAGES " + str(count)
    l = Label(t, text=msg, fg="blue").place(x=130, y=240)
    ai = Button(t, text="ADD IMAGES", fg="blue", command=lambda: capture(path,t)).place(x=30, y=240)
def create(id,top):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')
    path = os.path.join(path,id)
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            addimage(top,path)
        else:
            engine.say("UNABLE TO ADD")
            engine.runAndWait()
    except OSError:
        print('Error:Creating Directory. '+path)
def capture(path,t):
    global count
    count = count + 1
    if(count>20):
        destroyadd(t)
        count=0
    else:
        msg = "NO OF IMAGES " + str(count)
        l = Label(t, text=msg, fg="blue").place(x=130, y=240)
        cap=cv2.VideoCapture(0)
        ret,frame=cap.read()
        msg="img"+str(count)+".png"
        p=os.path.join(path,msg)
        cv2.imwrite(p,frame)
        cap.release()
        cv2.destroyAllWindows()
'''
DESTROY WINDOW
'''
def destroyadd(win):
    win.destroy()
    global conn
    global namevalue
    global idvalue
    global emailvalue
    global passwordvalue
    cursor = conn.cursor()
    sql = "INSERT INTO users(id,user,password,email) VALUES (%s,%s,%s,%s)"
    values = (idvalue, namevalue, passwordvalue, emailvalue)
    cursor.execute(sql, values)
    conn.commit()
    if (cursor.rowcount != 0):
        time.sleep(1)
        msg="ADDED ID"+idvalue+"TO DATABASE"
        engine.say(msg)
        engine.runAndWait()
    else:
        engine.say("UNABLE TO ADD")
        engine.runAndWait()
    # engine.say("THANK YOU")
    # engine.runAndWait()
'''
LEAVE
'''
def leave():
    engine.say("THANK YOU")
    engine.runAndWait()
    exit()
'''
CREATING THE GUI PART
'''
engine = pyttsx3.init()
first=Tk()
first.geometry("300x250")
name=StringVar()
password=StringVar()
email=StringVar()
id=StringVar()
connect()
a = Button(first, text="ADD", fg="green",command=lambda:add(first)).place(x=10, y=100)
d = Button(first, text="DELETE", fg="red",command=lambda:delete(first)).place(x=70, y=100)
u = Button(first, text="UPDATE", fg="orange",command=lambda:update(first)).place(x=140, y=100)
le = Button(first, text="LEAVE", fg="blue", command=leave).place(x=210, y=100)
first.mainloop()
