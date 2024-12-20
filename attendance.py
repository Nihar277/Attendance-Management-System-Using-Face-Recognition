import tkinter as tk
from tkinter import *
import os, cv2
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import pyttsx3 

# Project modules
import show_attendance
import takeImage
import trainImage
import automaticAttedance

# Paths
haarcasecade_path = "D:\\CHARUSAT\\College Projects\\Attendance-Management-system-using-face-recognition\\haarcascade_frontalface_default.xml"
trainimagelabel_path = "D:\\CHARUSAT\\College Projects\\Attendance-Management-system-using-face-recognition\\TrainingImageLabel\\Trainner.yml"
trainimage_path = "D:\\CHARUSAT\\College Projects\\Attendance-Management-system-using-face-recognition\\TrainingImage"
studentdetail_path = "D:\\CHARUSAT\\College Projects\\Attendance-Management-system-using-face-recognition\\StudentDetails\\studentdetails.csv"
attendance_path = "D:\\CHARUSAT\\College Projects\\Attendance-Management-system-using-face-recognition\\Attendance"

# Text-to-speech initialization
def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()

# Main window setup
window = Tk()
window.title("Face Recognizer")
window.geometry("1280x720")
window.configure(background="#f0f0f0")

# Logo and title
logo = Image.open('D:\\CHARUSAT\\College Projects\\Attendance-Management-system-using-face-recognition\\UI_Image\\0001.png')
logo = logo.resize((50, 47), Image.Resampling.LANCZOS)
logo1 = ImageTk.PhotoImage(logo)
titl = tk.Label(window, bg="#f0f0f0", relief=RIDGE, bd=10, font=("Arial", 35))
titl.pack(fill=X)
l1 = tk.Label(window, image=logo1, bg="#f0f0f0")
l1.place(x=470, y=10)
titl = tk.Label(window, text="Smart College!!", bg="#f0f0f0", fg="#333", font=("Arial", 27))
titl.place(x=525, y=12)

# Welcome message
a = tk.Label(
    window,
    text="Welcome to the Face Recognition Based\nAttendance Management System",
    bg="#f0f0f0",
    fg="#444",
    bd=10,
    font=("Arial", 35)
)
a.pack()

# Images for buttons
ri = Image.open("D:\\CHARUSAT\\College Projects\\Attendance-Management-system-using-face-recognition\\UI_Image\\register.png")
r = ImageTk.PhotoImage(ri)
label1 = Label(window, image=r, bg="#f0f0f0")
label1.image = r
label1.place(x=100, y=270)

ai = Image.open("D:\\CHARUSAT\\College Projects\\Attendance-Management-system-using-face-recognition\\UI_Image\\attendance.png")
a = ImageTk.PhotoImage(ai)
label2 = Label(window, image=a, bg="#f0f0f0")
label2.image = a
label2.place(x=980, y=270)

vi = Image.open("D:\\CHARUSAT\\College Projects\\Attendance-Management-system-using-face-recognition\\UI_Image\\verifyy.png")
v = ImageTk.PhotoImage(vi)
label3 = Label(window, image=v, bg="#f0f0f0")
label3.image = v
label3.place(x=600, y=270)

# Helper function to validate input
def testVal(inStr, acttyp):
    if acttyp == "1" and not inStr.isdigit():  # insert
        return False
    return True

# Error message for missing input
def err_screen():
    sc1 = tk.Tk()
    sc1.geometry("300x110")
    sc1.title("Warning!!")
    sc1.configure(background="#f0f0f0")
    sc1.resizable(0, 0)
    tk.Label(sc1, text="Enrollment & Name required!!!", fg="#333", bg="#f0f0f0", font=("Arial", 20, "bold")).pack()
    tk.Button(sc1, text="OK", command=sc1.destroy, fg="#f0f0f0", bg="#333", width=9, height=1, font=("Arial", 20, "bold")).place(x=110, y=50)

# Function to open the student registration UI
def TakeImageUI():
    ImageUI = Tk()
    ImageUI.title("Take Student Image..")
    ImageUI.geometry("780x480")
    ImageUI.configure(background="#f0f0f0")
    ImageUI.resizable(0, 0)
    
    tk.Label(ImageUI, text="Register Your Face", bg="#f0f0f0", fg="#333", font=("Arial", 30)).pack(fill=X)
    tk.Label(ImageUI, text="Enter the details", bg="#f0f0f0", fg="#444", font=("Arial", 24)).place(x=280, y=75)

    # Enrollment number
    tk.Label(ImageUI, text="Enrollment No", bg="#f0f0f0", fg="#444", font=("Arial", 12)).place(x=120, y=130)
    txt1 = tk.Entry(ImageUI, validate="key", bg="#f0f0f0", fg="#444", font=("Arial", 25, "bold"))
    txt1.place(x=250, y=130)
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    # Name
    tk.Label(ImageUI, text="Name", bg="#f0f0f0", fg="#444", font=("Arial", 12)).place(x=120, y=200)
    txt2 = tk.Entry(ImageUI, bg="#f0f0f0", fg="#444", font=("Arial", 25, "bold"))
    txt2.place(x=250, y=200)

    # Notification
    tk.Label(ImageUI, text="Notification", bg="#f0f0f0", fg="#444", font=("Arial", 12)).place(x=120, y=270)
    message = tk.Label(ImageUI, text="", bg="#f0f0f0", fg="#444", font=("Arial", 12, "bold"))
    message.place(x=250, y=270)

    def take_image():
        takeImage.TakeImage(txt1.get(), txt2.get(), haarcasecade_path, trainimage_path, message, err_screen, text_to_speech)
        txt1.delete(0, "end")
        txt2.delete(0, "end")

    tk.Button(ImageUI, text="Take Image", command=take_image, bg="#333", fg="#f0f0f0", font=("Arial", 18)).place(x=130, y=350)

    def train_image():
        trainImage.TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech)

    tk.Button(ImageUI, text="Train Image", command=train_image, bg="#333", fg="#f0f0f0", font=("Arial", 18)).place(x=360, y=350)

# Function to open the automatic attendance UI
def automatic_attendance():
    automaticAttedance.subjectChoose(text_to_speech)

# Function to view attendance
def view_attendance():
    show_attendance.subjectchoose(text_to_speech)

# Main buttons
tk.Button(window, text="Register a new student", command=TakeImageUI, bg="#333", fg="#f0f0f0", font=("Arial", 16)).place(x=100, y=520)
tk.Button(window, text="Take Attendance", command=automatic_attendance, bg="#333", fg="#f0f0f0", font=("Arial", 16)).place(x=600, y=520)
tk.Button(window, text="View Attendance", command=view_attendance, bg="#333", fg="#f0f0f0", font=("Arial", 16)).place(x=1000, y=520)
tk.Button(window, text="EXIT", command=quit, bg="#333", fg="#f0f0f0", font=("Arial", 16)).place(x=600, y=660)

window.mainloop()
