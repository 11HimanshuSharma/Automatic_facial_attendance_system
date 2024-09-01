import cv2
import face_recognition
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox, Frame, filedialog
import getreport
import database
import util
import numpy as np


class FaceScannerApp(Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller

        self.parent = parent
        self.parent.title("Video Scanner")
        self.parent.geometry("1200x520+350+100")

        self.main_frame = Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.upload_video_button = util.get_button(self.main_frame, "Upload Video", 'blue', self.upload_video)
        self.upload_video_button.place(x=750, y=20)

        self.stop_video_button = util.get_button(self.main_frame, "Stop Video", 'purple', self.stop_video)
        self.stop_video_button.place(x=750, y=120)

        self.mark_attendance_button = util.get_button(self.main_frame, "Mark Attendance Now", 'green', self.mark_attendance)
        self.mark_attendance_button.place(x=750, y=220)

        self.get_report_button = util.get_button(self.main_frame, "Get Updated Report", 'orange', self.get_report)
        self.get_report_button.place(x=750, y=320)

        self.close_button = util.get_button(self.main_frame, "Close", 'red', self.close)
        self.close_button.place(x=750, y=420)

        self.video_label = tk.Label(self.main_frame)
        self.video_label.place(x=10, y=0, width=700, height=500)

        self.get_report_main_frame = None

        self.identified_students_list = []

        self.video_capture = None
        self.update_delay = 10
        self.tk_image = None

    def close(self):
        self.stop_video()
        self.parent.destroy()

    def get_report(self):
        self.stop_video()
        if self.get_report_main_frame:
            self.get_report_main_frame.pack()
        else:
            self.get_report_main_frame = IdentifiedStudentsReport(self.parent, self.identified_students_list)
            self.get_report_main_frame.pack()

    def upload_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi")])
        if file_path:
            self.start_video_capture(file_path)

    def start_video_capture(self, video_path):
        self.video_capture = cv2.VideoCapture(video_path)
        self.update_frame()

    def stop_video(self):
        if self.video_capture:
            self.video_capture.release()
            self.video_capture = None
        self.video_label.config(image='')
        print(self.identified_students_list)

    def update_frame(self):
        if self.video_capture:
            ret, frame = self.video_capture.read()
            if ret:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

                face_locations = face_recognition.face_locations(rgb_small_frame)
                # print(f"Detected faces: {face_locations}")

                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                self.store_identified_students(face_encodings)
                print(face_encodings)

                face_locations = [(top*4, right*4, bottom*4, left*4) for (top, right, bottom, left) in face_locations]

                for (top, right, bottom, left) in face_locations:
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                pil_image = pil_image.resize((800, 500), Image.LANCZOS)
                self.tk_image = ImageTk.PhotoImage(image=pil_image)

                self.video_label.config(image=self.tk_image)

            self.main_frame.after(self.update_delay, self.update_frame)

    def store_identified_students(self, face_encodings):
        if face_encodings:
            known_face_encodings, known_face_metadata = database.know_face_encodings()

            if known_face_encodings:
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

                    if matches:
                        best_match_index = np.argmin(face_distances)

                        if best_match_index < len(matches) and matches[best_match_index][0]:
                            self.identified_students_list.append(known_face_metadata[best_match_index])

    def mark_attendance(self):
        print(self.identified_students_list)
        self.stop_video()
        if self.identified_students_list:
            for student in self.identified_students_list:
                student_id = student['student_id']
                database.mark_attendance(student_id)
            self.show_message("Identified Students","Attendance Marked successfully")
        else:
            self.show_message("Identified Power", "No matching face found")

    def show_message(self, title, message):
        messagebox.showinfo(title, message)


class IdentifiedStudentsReport(tk.Frame):
    def __init__(self, parent, identified_students_list):
        super().__init__(parent)
        self.identified_students_list = identified_students_list

        self.parent = parent
        self.parent.title("Identified Students")
        self.parent.geometry("600x520+350+100")

        self.identified_students_frame = tk.Frame(self)
        self.identified_students_frame.pack(fill=tk.BOTH, expand=True)

        self.label = tk.Label(self.identified_students_frame, text="Identified Students", font=("Arial", 18))
        self.label.pack(pady=20)

        self.scrollbar = tk.Scrollbar(self.identified_students_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(self.identified_students_frame, yscrollcommand=self.scrollbar.set, font=("Arial", 12), width=100)
        self.listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.listbox.yview)

        self.mark_attendance_button = util.get_button(self.identified_students_frame, "Mark Attendance Now", 'green', self.mark_attendance)
        self.mark_attendance_button.pack(pady=10)
        self.mark_attendance_button.config(height=1)

        self.get_updated_report_button = util.get_button(self.identified_students_frame, "Get Updated Report", 'orange', self.get_report)
        self.get_updated_report_button.pack(pady=10)
        self.get_updated_report_button.config(height=1)

        self.close_button = util.get_button(self.identified_students_frame, "Close", 'red', self.close)
        self.close_button.pack(pady=10)
        self.close_button.config(height=1)

        for student in self.identified_students_list:
            student_id = student['student_id']
            name = student['name']
            roll_number = student['roll_number']
            attendance = student['attendance']

            formatted_string = f"ID: {student_id:<10} Name: {name:<40} Roll Number: {roll_number:<15} Attendance: {attendance:<15}"
            self.listbox.insert(tk.END, formatted_string)

    def close(self):
        self.parent.destroy()

    def get_report(self):
        if self.get_report_main_frame:
            self.get_report_main_frame.pack()
        else:
            self.get_report_main_frame = getreport.AttendanceReportApp(self.parent, self)
            self.get_report_main_frame.pack(fill=tk.BOTH, expand=True)

    def mark_attendance(self):
        if self.identified_students_list:
            for student in self.identified_students_list:
                student_id = student['student_id']
                database.mark_attendance(student_id)
        else:
            self.show_message("Identified Power", "No matching face found")

    def show_message(self, title, message):
        messagebox.showinfo(title, message)


if __name__ == "__main__":
    root = tk.Tk()
    app = FaceScannerApp(root)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
