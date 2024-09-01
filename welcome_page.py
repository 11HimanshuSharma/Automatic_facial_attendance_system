import tkinter as tk
from tkinter import Frame, Label
import login
import util
import face_recognition
import os
import site
import sys

class App:
    def __init__(self, root):
        self.root = root

        self.root.geometry("900x480+350+100")
        self.root.title("Mark student Attendance")

        self.main_frame = Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.label = Label(self.main_frame, text="Mark Students Attendance", font=("Comic Sans MS", 50))
        self.label.pack(pady=10)  

        self.login_button_main_frame = util.get_button(
            self.main_frame, 'Teacher login', 'green', self.show_login_frame)
        self.login_button_main_frame.place(x=290, y=200)

        self.close_button_main_frame = util.get_button(self.main_frame, "Close", 'red', self.close)
        self.close_button_main_frame.place(x=290, y=330)

        self.login_frame = None

    def show_login_frame(self):
        self.main_frame.pack_forget()
        
        if self.login_frame:
            self.login_frame.pack()
        else:
            self.login_frame = login.LoginWindow(self.root, self)
            self.login_frame.pack()

    def close(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
