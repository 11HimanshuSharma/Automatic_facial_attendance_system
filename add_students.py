import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import face_recognition
import util
import database

class RegisterApp(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        
        self.parent = parent
        self.parent.title("Register New User")
        self.parent.geometry("900x480+350+100")
        
        self.font = ("Arial", 12)
        
        self.frame = tk.Frame(self.parent)
        self.frame.pack(pady=20)
        
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)

        self.student_name = tk.Label(self.frame, text="Name:", font=self.font, width=30)
        self.student_name.grid(row=0, column=0, padx=10, pady=30, sticky='e')
        self.student_name_entry = tk.Entry(self.frame, font=self.font, width=40)
        self.student_name_entry.grid(row=0, column=1, padx=10, pady=30, sticky='w')
        
        self.student_rollno = tk.Label(self.frame, text="Roll Number:", font=self.font, width=30)
        self.student_rollno.grid(row=1, column=0, padx=10, pady=30, sticky='e')
        self.student_rollno_entry = tk.Entry(self.frame, font=self.font, width=40)
        self.student_rollno_entry.grid(row=1, column=1, padx=10, pady=30, sticky='w')

        self.upload_button = util.get_button(self.frame, "Upload Image", 'blue', lambda: self.open_upload_window('upload'))
        self.upload_button.grid(row=2, column=0, padx=10, pady=20, sticky='ew')

        self.capture_button = util.get_button(self.frame, "Capture Image", 'green', lambda: self.open_upload_window('capture'))
        self.capture_button.grid(row=2, column=1, padx=10, pady=20, sticky='ew')

        self.save_button = util.get_button(self.frame, "Save", 'green', self.save_student)
        self.save_button.grid(row=4, columnspan=2, padx=10, pady=20, sticky='ew')

        self.canvas = tk.Canvas(self.parent, width=800, height=500)
        self.canvas.pack()

        self.most_recent_capture_arr = None

        database.initialize_db()

    def open_upload_window(self, mode):
        self.upload_window = UploadImageWindow(self, mode)
        self.upload_window.upload_image_window.mainloop()

    def update_image(self, image):
        self.most_recent_capture_arr = image
        # self.display_image(self.most_recent_capture_arr)

    # def display_image(self, image):
    #     rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #     pil_image = Image.fromarray(rgb_image)
    #     pil_image = pil_image.resize((800, 500), Image.LANCZOS)
    #     self.tk_image = ImageTk.PhotoImage(pil_image)
    #     self.canvas.create_image(0, 0, image=self.tk_image, anchor=tk.NW)

    def save_student(self):
        name = self.student_name_entry.get()
        roll_number = self.student_rollno_entry.get()
        if self.most_recent_capture_arr is not None:
            rgb_image = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_image)
            if face_locations:
                face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
                for (top, right, bottom, left) in face_locations:
                    cv2.rectangle(rgb_image, (left, top), (right, bottom), (0, 255, 0), 2)
                pil_image = Image.fromarray(rgb_image)
                pil_image = pil_image.resize((800, 500), Image.LANCZOS)
                self.tk_image = ImageTk.PhotoImage(pil_image)
                self.canvas.create_image(0, 0, image=self.tk_image, anchor=tk.NW)
                
               
                
                database.add_student(name,roll_number,face_encodings)
                util.msg_box('success',"Student successfully added.")
                database.add_student(name, roll_number, face_encodings)
                self.student_name_entry.delete(0, tk.END)
                self.student_rollno_entry.delete(0, tk.END)
                self.most_recent_capture_arr = None
            else:
                util.msg_box('Error', 'No faces found in the image.')
        else:
            util.msg_box('Error', 'No image captured or uploaded.')

class UploadImageWindow:
    def __init__(self, main_app, mode):
        self.main_app = main_app
        self.mode = mode
        self.upload_image_window = tk.Toplevel()
        self.upload_image_window.geometry("1200x520+350+100")
        self.upload_image_window.title("Upload or Capture Image")

        if self.mode == 'upload':
            self.upload_button = util.get_button(self.upload_image_window, "Select Image", 'green', self.upload_image)
            self.upload_button.place(x=750, y=75)
        elif self.mode == 'capture':
            self.capture_button = util.get_button(self.upload_image_window, "Capture Image", 'green', self.toggle_capture_image)
            self.capture_button.place(x=750, y=75)

        self.save_button = util.get_button(self.upload_image_window, "Add Image", 'blue', self.add_image_to_main)
        self.save_button.place(x=750, y=200)

        self.try_again_button = util.get_button(self.upload_image_window, "Try Again", 'blue', self.try_again)
        self.try_again_button.place(x=750, y=325)

        self.upload_image_label = tk.Label(self.upload_image_window)
        self.upload_image_label.place(x=10, y=0, width=700, height=500)

        self.most_recent_capture_arr = None
        self.cap = None
        self.is_capturing = False

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.most_recent_capture_arr = cv2.imread(file_path)
            self.display_image(self.most_recent_capture_arr)

    def toggle_capture_image(self):
        if self.is_capturing:
            self.stop_capture_image()
        else:
            self.start_capture_image()

    def start_capture_image(self):
        self.cap = cv2.VideoCapture(0)
        self.is_capturing = True
        self.capture_image()

    def stop_capture_image(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.is_capturing = False

    def capture_image(self):
        if self.is_capturing:
            ret, frame = self.cap.read()
            if ret:
                self.most_recent_capture_arr = frame
                self.display_image(self.most_recent_capture_arr)
            self.upload_image_window.after(10, self.capture_image)

    def try_again(self):
        if self.mode == 'upload':
            self.upload_image()
        elif self.mode == 'capture':
            self.start_capture_image()

    def display_image(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)
        pil_image = pil_image.resize((700, 500), Image.LANCZOS)
        photo = ImageTk.PhotoImage(pil_image)
        self.upload_image_label.config(image=photo)
        self.upload_image_label.image = photo
        self.draw_rectangle_on_image()

    def draw_rectangle_on_image(self):
        if self.most_recent_capture_arr is not None:
            rgb_image = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_image)
            if face_locations:
                for (top, right, bottom, left) in face_locations:
                    cv2.rectangle(rgb_image, (left, top), (right, bottom), (0, 255, 0), 2)
                pil_image = Image.fromarray(rgb_image)
                pil_image = pil_image.resize((700, 500), Image.LANCZOS)
                photo = ImageTk.PhotoImage(pil_image)
                self.upload_image_label.config(image=photo)
                self.upload_image_label.image = photo

    def add_image_to_main(self):
        if self.most_recent_capture_arr is not None:
            self.main_app.update_image(self.most_recent_capture_arr)
            self.upload_image_window.destroy()
            util.msg_box("Image uploadeding....", "Image uploaded")

if __name__ == "__main__":
    root = tk.Tk()
    app = RegisterApp(root)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
