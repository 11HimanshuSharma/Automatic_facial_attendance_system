import tkinter as tk
import util
from tkinter import Frame, Label, Entry
import subprocess
import os
import face_recognition
import welcome_page
import sys
import site

import teacher
import mode_select

class LoginWindow(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.parent = parent
        self.parent.title("Login Form")
        self.parent.geometry("900x480+350+100")
        
        self.main_frame = Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.label = Label(self.main_frame, text="Enter UserName & Password", font=("Comic Sans MS", 50))
        self.label.pack(pady=9)
        
        self.frame = tk.Frame(self.main_frame)
        self.frame.pack(pady=10)
        
        self.font = ("Arial", 12)
     
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        
        self.username_label = tk.Label(self.frame, text="Username:", font=self.font, width=30)
        self.username_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.username_entry = tk.Entry(self.frame, font=self.font, width=40)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        

        self.password_label = tk.Label(self.frame, text="Password:", font=self.font, width=30)
        self.password_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.password_entry = tk.Entry(self.frame, show="*", font=self.font, width=40)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        
        self.submit_button = util.get_button(self.frame, "Submit", 'green', self.submit)
        self.submit_button.grid(row=2, column=0, columnspan=2, pady=50, sticky='n')
        
        
        self.mode_frame = None
        
    def select_mode(self):
        self.frame.pack_forget()
        
        if self.mode_frame:
            self.mode_frame.pack()
        else:
            self.mode_frame = teacher.Teacher(self.parent,self)
            self.mode_frame.pack()
        


    def submit(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        print(f"Username: {username}, Password: {password}")
        
        # yhe per tum log apna login credientials verificatin code likh sakte ho
        # here you can write your login auth code
        #example
        # if username in teacher_usernames:
        #     self.select_mode
        #else:
        #     util.msg_box("Try Again","Username or password incorrect, please login again")
        #     self.try_again()
        
        self.select_mode()
        
        
        
        
        self.destroy()  
        
    # def try_again(self):
    #     self.username_entry.delete(0, tk.END)
    #     self.password_entry.delete(0, tk.END)
        

if __name__ == "__main__":
    root = tk.Tk()
    login_window = LoginWindow(root, None)
    login_window.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
