# # import cv2
# # import numpy as np
# # from pymongo import MongoClient
# #
# # client = MongoClient('mongodb://localhost:27017/')  # Connect to MongoDB
# # db = client['SE_ADMIN']  # Replace 'your_database_name' with your MongoDB database name
# # collection = db['students']  # Collection for storing student data
# #
# # faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# # cam = cv2.VideoCapture(0)
# #
# # def insert_or_update(Id, Name, age):
# #     student = collection.find_one({'Id': Id})
# #     if student:
# #         collection.update_one({'Id': Id}, {'$set': {'Name': Name, 'age': age}})
# #     else:
# #         collection.insert_one({'Id': Id, 'Name': Name, 'age': age})
# #
# # def create_dataset(Id, Name, age):
# #     sample_num = 0
# #     while True:
# #         ret, img = cam.read()
# #         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# #         faces = faceDetect.detectMultiScale(gray, 1.3, 5)
# #         for (x, y, w, h) in faces:
# #             sample_num += 1
# #             cv2.imwrite(f"dataset/user.{Id}.{sample_num}.jpg", gray[y:y+h, x:x+w])
# #             cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
# #             cv2.waitKey(100)
# #         cv2.imshow("Face", img)
# #         cv2.waitKey(1)
# #         if sample_num > 20:
# #             break
# #
# #     insert_or_update(Id, Name, age)
# #     cam.release()
# #     cv2.destroyAllWindows()
# #
# # # Input student details
# # Id = input("Enter User Id: ")
# # Name = input("Enter User Name: ")
# # age = input("Enter User Age: ")
# # create_dataset(Id, Name, age)
#
#
# import cv2
# import numpy as np
# from pymongo import MongoClient
# import tkinter as tk
# from tkinter import simpledialog
#
# # MongoDB connection
# client = MongoClient('mongodb://localhost:27017/')
# db = client['SE_ADMIN']
# collection = db['students']
#
# # OpenCV face detection setup
# faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# cam = cv2.VideoCapture(0)
#
# # Function to insert or update student data in MongoDB
# def insert_or_update(Id, Name, age):
#     student = collection.find_one({'Id': Id})
#     if student:
#         collection.update_one({'Id': Id}, {'$set': {'Name': Name, 'age': age}})
#     else:
#         collection.insert_one({'Id': Id, 'Name': Name, 'age': age})
#
# # Function to create dataset with face images
# def create_dataset(Id, Name, age):
#     sample_num = 0
#     while True:
#         ret, img = cam.read()
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         faces = faceDetect.detectMultiScale(gray, 1.3, 5)
#         for (x, y, w, h) in faces:
#             sample_num += 1
#             cv2.imwrite(f"dataset/user.{Id}.{sample_num}.jpg", gray[y:y+h, x:x+w])
#             cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
#             cv2.waitKey(100)
#         cv2.imshow("Face", img)
#         cv2.waitKey(1)
#         if sample_num > 20:
#             break
#
#     insert_or_update(Id, Name, age)
#     cam.release()
#     cv2.destroyAllWindows()
#
# # Tkinter GUI for inputting student details and capturing images
# def capture_student_data():
#     root = tk.Tk()
#     root.title("Student Details Capture")
#
#     # Function to handle button click and capture data
#     def capture_data():
#         Id = entry_id.get()
#         Name = entry_name.get()
#         age = entry_age.get()
#
#         if Id and Name and age:
#             create_dataset(Id, Name, age)
#
#     # GUI layout
#     label_id = tk.Label(root, text="Enter User Id:")
#     label_id.pack()
#     entry_id = tk.Entry(root)
#     entry_id.pack()
#
#     label_name = tk.Label(root, text="Enter User Name:")
#     label_name.pack()
#     entry_name = tk.Entry(root)
#     entry_name.pack()
#
#     label_age = tk.Label(root, text="Enter User Age:")
#     label_age.pack()
#     entry_age = tk.Entry(root)
#     entry_age.pack()
#
#     button_capture = tk.Button(root, text="Capture Data", command=capture_data)
#     button_capture.pack()
#
#     root.mainloop()
#
# # Main function to start the process
# if __name__ == "__main__":
#     capture_student_data()

#
# import cv2
# import numpy as np
# from pymongo import MongoClient
# import tkinter as tk
# from tkinter import simpledialog, messagebox
#
# # MongoDB connection
# client = MongoClient('mongodb://localhost:27017/')
# db = client['SE_ADMIN']
# collection = db['students']
#
# # OpenCV face detection setup
# faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# cam = cv2.VideoCapture(0)
#
# # Function to insert or update student data in MongoDB
# def insert_or_update(Id, Name, age):
#     student = collection.find_one({'Id': Id})
#     if student:
#         collection.update_one({'Id': Id}, {'$set': {'Name': Name, 'age': age}})
#     else:
#         collection.insert_one({'Id': Id, 'Name': Name, 'age': age, 'status': 'NO'})
#
# # Function to create dataset with face images
# def create_dataset(Id, Name, age):
#     sample_num = 0
#     while True:
#         ret, img = cam.read()
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         faces = faceDetect.detectMultiScale(gray, 1.3, 5)
#         for (x, y, w, h) in faces:
#             sample_num += 1
#             cv2.imwrite(f"dataset/user.{Id}.{sample_num}.jpg", gray[y:y+h, x:x+w])
#             cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
#             cv2.waitKey(100)
#         cv2.imshow("Face", img)
#         cv2.waitKey(1)
#         if sample_num > 20:
#             break
#
#     insert_or_update(Id, Name, age)
#     cam.release()
#     cv2.destroyAllWindows()
#
# # Function to show success message
# def show_success_message():
#     messagebox.showinfo("Registration Complete", "Voter has been successfully registered!")
#
# # Tkinter GUI for inputting student details and capturing images
# def capture_student_data():
#     root = tk.Tk()
#     root.title("Voter Registration")
#
#     # Centering the window on screen
#     window_width = 400
#     window_height = 250
#     screen_width = root.winfo_screenwidth()
#     screen_height = root.winfo_screenheight()
#     x = int((screen_width/2) - (window_width/2))
#     y = int((screen_height/2) - (window_height/2))
#     root.geometry(f'{window_width}x{window_height}+{x}+{y}')
#
#     # Styling the window
#     root.configure(bg='#f0f0f0')  # Light gray background color
#
#     # Function to handle button click and capture data
#     def capture_data():
#         Id = entry_id.get()
#         Name = entry_name.get()
#         age = entry_age.get()
#
#         if Id and Name and age:
#             create_dataset(Id, Name, age)
#             root.destroy()
#             show_success_message()
#
#     # GUI layout
#     label_id = tk.Label(root, text="Enter NIC:", bg='#f0f0f0')  # Light gray background for labels
#     label_id.pack()
#     entry_id = tk.Entry(root)
#     entry_id.pack()
#
#     label_name = tk.Label(root, text="Enter Name:", bg='#f0f0f0')
#     label_name.pack()
#     entry_name = tk.Entry(root)
#     entry_name.pack()
#
#     label_age = tk.Label(root, text="Enter Age:", bg='#f0f0f0')
#     label_age.pack()
#     entry_age = tk.Entry(root)
#     entry_age.pack()
#
#     button_capture = tk.Button(root, text="Capture Data", command=capture_data, bg='#4CAF50', fg='white')  # Green button
#     button_capture.pack(pady=10)
#
#     root.mainloop()
#
# # Main function to start the process
# if __name__ == "__main__":
#     capture_student_data()
#
#


# import cv2
# import numpy as np
# from pymongo import MongoClient
# import tkinter as tk
# from tkinter import simpledialog, messagebox
# from PIL import Image, ImageTk
#
# # MongoDB connection
# client = MongoClient('mongodb://localhost:27017/')
# db = client['SE_ADMIN']
# collection = db['students']
#
# # OpenCV face detection setup
# faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# cam = cv2.VideoCapture(0)
#
# # Function to insert or update student data in MongoDB
# def insert_or_update(Id, Name, age):
#     student = collection.find_one({'Id': Id})
#     if student:
#         collection.update_one({'Id': Id}, {'$set': {'Name': Name, 'age': age}})
#     else:
#         collection.insert_one({'Id': Id, 'Name': Name, 'age': age, 'status': 'NO'})
#
# # Function to create dataset with face images
# def create_dataset(Id, Name, age):
#     sample_num = 0
#     while True:
#         ret, img = cam.read()
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         faces = faceDetect.detectMultiScale(gray, 1.3, 5)
#         for (x, y, w, h) in faces:
#             sample_num += 1
#             cv2.imwrite(f"dataset/user.{Id}.{sample_num}.jpg", gray[y:y+h, x:x+w])
#             cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
#             cv2.waitKey(100)
#         cv2.imshow("Face", img)
#         cv2.waitKey(1)
#         if sample_num > 50:
#             break
#
#     insert_or_update(Id, Name, age)
#     cam.release()
#     cv2.destroyAllWindows()
#
# # Function to show success message
# def show_success_message():
#     messagebox.showinfo("Registration Complete", "Voter has been successfully registered!")
#
# # Tkinter GUI for inputting student details and capturing images
# def capture_student_data():
#     root = tk.Tk()
#     root.title("Voter Registration")
#
#     # Centering the window on screen
#     window_width = 500
#     window_height = 350
#     screen_width = root.winfo_screenwidth()
#     screen_height = root.winfo_screenheight()
#     x = int((screen_width/2) - (window_width/2))
#     y = int((screen_height/2) - (window_height/2))
#     root.geometry(f'{window_width}x{window_height}+{x}+{y}')
#
#     # Load background image
#     bg_image = Image.open("background.jpg")
#     bg_photo = ImageTk.PhotoImage(bg_image)
#
#     # Create canvas to display the background image
#     canvas = tk.Canvas(root, width=window_width, height=window_height)
#     canvas.pack(fill="both", expand=True)
#     canvas.create_image(0, 0, image=bg_photo, anchor="nw")
#
#     # Function to handle button click and capture data
#     def capture_data():
#         Id = entry_id.get()
#         Name = entry_name.get()
#         age = entry_age.get()
#
#         if Id and Name and age:
#             create_dataset(Id, Name, age)
#             root.destroy()
#             show_success_message()
#
#     # GUI layout on the canvas
#     label_font = ('Roboto', 12)
#     label_id = tk.Label(root, text="Enter NIC (Without last V):", bg='#f0f0f0', font=label_font)  # Light gray background for labels
#     canvas.create_window(250, 50, window=label_id)  # Adjust position as needed
#     entry_id = tk.Entry(root)
#     canvas.create_window(250, 80, window=entry_id)  # Adjust position as needed
#
#     label_name = tk.Label(root, text="Enter Name with initials:", bg='#f0f0f0',font=label_font)
#     canvas.create_window(250, 110, window=label_name)  # Adjust position as needed
#     entry_name = tk.Entry(root)
#     canvas.create_window(250, 140, window=entry_name)  # Adjust position as needed
#
#     label_age = tk.Label(root, text="Enter Zonal Number:", bg='#f0f0f0',font=label_font)
#     canvas.create_window(250, 170, window=label_age)  # Adjust position as needed
#     entry_age = tk.Entry(root)
#     canvas.create_window(250, 200, window=entry_age)  # Adjust position as needed
#
#     button_capture = tk.Button(root, text="Capture Data", command=capture_data, bg='#4CAF50', fg='white')  # Green button
#     canvas.create_window(250, 230, window=button_capture)  # Adjust position as needed
#
#     root.mainloop()
#
# # Main function to start the process
# if __name__ == "__main__":
#     capture_student_data()

import cv2
import numpy as np
import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import csv
import os

# OpenCV face detection setup
faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)

# CSV file path
csv_file = 'voters.csv'

# Function to insert or update student data in CSV
def insert_or_update(Id, Name, age):
    # Read the existing data
    data = []
    if os.path.isfile(csv_file):
        with open(csv_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)
    else:
        # Initialize file with headers if it doesn't exist
        with open(csv_file, 'w', newline='') as csvfile:
            fieldnames = ['Id', 'Name', 'age', 'status', 'fullName', 'birthday', 'district', 'zonal_name', 'gender']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    # Check if the student exists
    student_exists = False
    for student in data:
        if student['Id'] == Id:
            student['Name'] = Name
            student['age'] = age
            student_exists = True
            break

    # If student does not exist, add a new one
    if not student_exists:
        data.append({
            'Id': Id,
            'Name': Name,
            'age': age,
            'status': 'NO',
            'fullName': '',
            'birthday': '',
            'district': '',
            'zonal_name': '',
            'gender': ''
        })

    # Sort the data by the Name column
    data.sort(key=lambda x: x['Name'])

    # Write the sorted data back to the CSV file
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = ['Id', 'Name', 'age', 'status', 'fullName', 'birthday', 'district', 'zonal_name', 'gender']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Function to create dataset with face images
def create_dataset(Id, Name, age):
    sample_num = 0
    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            sample_num += 1
            cv2.imwrite(f"dataset/user.{Id}.{sample_num}.jpg", gray[y:y+h, x:x+w])
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.waitKey(100)
        cv2.imshow("Face", img)
        cv2.waitKey(1)
        if sample_num > 150:
            break

    insert_or_update(Id, Name, age)
    cam.release()
    cv2.destroyAllWindows()

# Function to show success message
def show_success_message():
    messagebox.showinfo("Registration Complete", "Voter has been successfully registered!")

# Tkinter GUI for inputting student details and capturing images
def capture_student_data():
    root = tk.Tk()
    root.title("Voter Registration")

    # Centering the window on screen
    window_width = 500
    window_height = 350
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width/2) - (window_width/2))
    y = int((screen_height/2) - (window_height/2))
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    # Load background image
    bg_image = Image.open("background.jpg")
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Create canvas to display the background image
    canvas = tk.Canvas(root, width=window_width, height=window_height)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Function to handle button click and capture data
    def capture_data():
        Id = entry_id.get()
        Name = entry_name.get()
        age = entry_age.get()

        if Id and Name and age:
            create_dataset(Id, Name, age)
            root.destroy()
            show_success_message()

    # GUI layout on the canvas
    label_font = ('Roboto', 12)
    label_id = tk.Label(root, text="Enter NIC (Without last V):", bg='#f0f0f0', font=label_font)  # Light gray background for labels
    canvas.create_window(250, 50, window=label_id)  # Adjust position as needed
    entry_id = tk.Entry(root)
    canvas.create_window(250, 80, window=entry_id)  # Adjust position as needed

    label_name = tk.Label(root, text="Enter Name with initials:", bg='#f0f0f0', font=label_font)
    canvas.create_window(250, 110, window=label_name)  # Adjust position as needed
    entry_name = tk.Entry(root)
    canvas.create_window(250, 140, window=entry_name)  # Adjust position as needed

    label_age = tk.Label(root, text="Enter Zonal Number:", bg='#f0f0f0', font=label_font)
    canvas.create_window(250, 170, window=label_age)  # Adjust position as needed
    entry_age = tk.Entry(root)
    canvas.create_window(250, 200, window=entry_age)  # Adjust position as needed

    button_capture = tk.Button(root, text="Capture Data", command=capture_data, bg='#4CAF50', fg='white')  # Green button
    canvas.create_window(250, 230, window=button_capture)  # Adjust position as needed

    root.mainloop()

# Main function to start the process
if __name__ == "__main__":
    capture_student_data()


