import csv
import tkinter as tk
from tkinter import *
import os
import cv2
import threading
import time
import datetime
import pandas as pd
import pyglet.media
from pathlib import Path

# Initialize sound
sound = pyglet.media.load("alarm.wav", streaming=False)

# Define paths using pathlib
base_path = Path("D:/CHARUSAT/College Projects/Attendance-Management-system-using-face-recognition")
haarcasecade_path = base_path / "haarcascade_frontalface_default.xml"
trainimagelabel_path = base_path / "TrainingImageLabel/Trainner.yml"
trainimage_path = base_path / "TrainingImage"
studentdetail_path = base_path / "StudentDetails/studentdetails.csv"
attendance_path = base_path / "Attendance"

# Play sound function
def play_sound():
    sound.play()

# Function to choose subject and fill attendance
def subjectChoose(text_to_speech):
    def fill_attendance():
        subject_name = subject_entry.get()
        if not subject_name:
            text_to_speech("Please enter the subject name!!!")
            return

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        try:
            recognizer.read(str(trainimagelabel_path))
        except:
            message = "Model not found, please train model"
            notification.configure(text=message, bg="black", fg="yellow", width=33, font=("times", 15, "bold"))
            notification.place(x=20, y=250)
            text_to_speech(message)
            return

        face_cascade = cv2.CascadeClassifier(str(haarcasecade_path))
        df = pd.read_csv(studentdetail_path)
        cam = cv2.VideoCapture(1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        col_names = ["Enrollment", "Name"]
        attendance = pd.DataFrame(columns=col_names)

        end_time = time.time() + 20  # Run for 20 seconds

        while time.time() < end_time:
            ret, frame = cam.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.2, 5)

            for (x, y, w, h) in faces:
                Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                if conf < 70:
                    name = df.loc[df["Enrollment"] == Id]["Name"].values[0]
                    attendance.loc[len(attendance)] = [Id, name]
                    label = f"{Id}-{name}"
                    color = (0, 255, 0)
                else:
                    label = "Unknown"
                    color = (0, 0, 255)
                    threading.Thread(target=play_sound).start()

                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label, (x, y - 10), font, 0.75, color, 2)

            cv2.imshow("Filling Attendance...", frame)
            if cv2.waitKey(1) & 0xFF == 27:  # Exit on pressing ESC
                break

        attendance.drop_duplicates(["Enrollment"], keep="first", inplace=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{subject_name}_{timestamp}.csv"
        attendance_file = attendance_path / subject_name / filename
        attendance.to_csv(attendance_file, index=False)

        message = f"Attendance Filled Successfully for {subject_name}"
        notification.configure(text=message, bg="black", fg="yellow", width=33, relief=RIDGE, bd=5, font=("times", 15, "bold"))
        text_to_speech(message)
        notification.place(x=20, y=250)

        cam.release()
        cv2.destroyAllWindows()

        # Display attendance in a new window
        display_attendance(attendance_file, subject_name)

    # Function to display attendance
    def display_attendance(file_path, subject_name):
        root = tk.Tk()
        root.title(f"Attendance of {subject_name}")
        root.configure(background="black")

        with open(file_path, newline="") as file:
            reader = csv.reader(file)
            for r, row in enumerate(reader):
                for c, cell in enumerate(row):
                    label = tk.Label(root, text=cell, width=10, height=1, fg="yellow", font=("times", 15, "bold"), bg="black", relief=tk.RIDGE)
                    label.grid(row=r, column=c)

        root.mainloop()

    # GUI setup for subject chooser
    subject_window = Tk()
    subject_window.title("Subject...")
    subject_window.geometry("580x320")
    subject_window.resizable(0, 0)
    subject_window.configure(background="black")

    title_label = tk.Label(subject_window, text="Enter the Subject Name", bg="black", fg="green", font=("arial", 25))
    title_label.pack(pady=20)

    subject_label = tk.Label(subject_window, text="Enter Subject", width=10, height=2, bg="black", fg="yellow", bd=5, relief=RIDGE, font=("times new roman", 15))
    subject_label.place(x=50, y=100)

    subject_entry = tk.Entry(subject_window, width=15, bd=5, bg="black", fg="yellow", relief=RIDGE, font=("times", 30, "bold"))
    subject_entry.place(x=190, y=100)

    fill_button = tk.Button(subject_window, text="Fill Attendance", command=fill_attendance, bd=7, font=("times new roman", 15), bg="black", fg="yellow", height=2, width=12, relief=RIDGE)
    fill_button.place(x=195, y=170)

    def open_attendance_folder():
        subject_name = subject_entry.get()
        if subject_name:
            os.startfile(attendance_path / subject_name)
        else:
            text_to_speech("Please enter the subject name!!!")

    check_sheets_button = tk.Button(subject_window, text="Check Sheets", command=open_attendance_folder, bd=7, font=("times new roman", 15), bg="black", fg="yellow", height=2, width=10, relief=RIDGE)
    check_sheets_button.place(x=360, y=170)

    global notification
    notification = tk.Label(subject_window, text="Attendance filled Successfully", bg="yellow", fg="black", width=33, height=2, font=("times", 15, "bold"))

    subject_window.mainloop()
