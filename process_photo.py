import cv2
import face_recognition
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import database
import util
import numpy as np
import getreport

class FaceScannerApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        
        self.parent.title("Process Image")
        self.parent.geometry("1200x520+350+100")
        
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.upload_image_button = util.get_button(self.main_frame, "Upload Image", 'blue', self.upload_image)
        self.upload_image_button.place(x=750, y=100)
        
        self.mark_attendance_button = util.get_button(self.main_frame, "Mark Attendance", 'green', self.mark_attendance)
        self.mark_attendance_button.place(x=750, y=200)
        
        self.get_report_button = util.get_button(self.main_frame,"Get Report",'orange', self.get_report)
        self.get_report_button.place(x = 750, y = 300)
        
        self.close_button = util.get_button(self.main_frame,"Close",'red', self.close)
        self.close_button.place(x = 750, y = 400)
        
        self.image_label = tk.Label(self.main_frame)
        self.image_label.place(x=10, y=0, width=700, height=500)
        
        self.most_recent_capture_arr = None
        
        self.get_report_main_frame = None
        
        
    def close(self):
        self.parent.destroy()
        
    def get_report(self):
        self.main_frame.pack_forget()
        
        if self.get_report_main_frame:
            self.get_report_main_frame.pack()
        else:
            self.get_report_main_frame = getreport.AttendanceReportApp(self.parent,self)
            self.get_report_main_frame.pack()
        
    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.most_recent_capture_arr = cv2.imread(file_path)
            self.display_image(self.most_recent_capture_arr)
            
    def display_image(self, image):
        self.rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(self.rgb_image)
        pil_image = pil_image.resize((700, 500), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(pil_image)
        self.image_label.config(image=self.photo)
        self.draw_rectangle_on_image() 

    def draw_rectangle_on_image(self):
        face_locations = face_recognition.face_locations(self.rgb_image)
        if face_locations:
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(self.rgb_image, (left, top), (right, bottom), (0, 255, 0), 2)
    
            pil_image = Image.fromarray(self.rgb_image)
            pil_image = pil_image.resize((700, 500), Image.LANCZOS)
            photo = ImageTk.PhotoImage(pil_image)
            self.image_label.config(image=photo)
            self.image_label.image = photo 
        else:
            self.show_message("No faces found in the image.")
        
    def mark_attendance(self):
        if self.most_recent_capture_arr is not None:
            rgb_image = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_image)
            face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
            print(face_encodings)

            if face_encodings:
                known_face_encodings, known_face_metadata = database.know_face_encodings()
                print(known_face_encodings)

                if known_face_encodings:
                    for face_encoding in face_encodings:
                        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                        print(matches)

   
                        matches_arr = np.array(matches)
                        if matches_arr.any():
                            best_match_index = np.argmin(face_distances)

                            if best_match_index < len(matches) and matches[best_match_index]:
                                student_id = known_face_metadata[best_match_index]["student_id"]
                                name = known_face_metadata[best_match_index]["name"]
                                roll_number = known_face_metadata[best_match_index]["roll_number"]

                                database.mark_attendance(student_id)

                                updated_attendance = database.get_attendance(student_id)
                                print(f"Updated Attendance for {name}, Roll No: {roll_number}: Total_attendance: {updated_attendance}")

                                self.show_message(f"Attendance marked for {name}, Roll No: {roll_number}")
                                return
                    self.show_message("No matching faces found.")
                else:
                    self.show_message("No known face encodings available.")
            else:
                self.show_message("No faces found in the image.")
        else:
            self.show_message("Please upload an image first.")

    
    def show_message(self, message):
        messagebox.showinfo("Attendance Marked", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceScannerApp(root, None)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
