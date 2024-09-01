import tkinter as tk
import sqlite3
import pickle
import util

class AttendanceReportApp(tk.Frame):
    def __init__(self, parent,controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.parent.title("Attendance Report")
        self.parent.geometry("600x520+350+100")

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.main_frame, text="Attendance Report", font=("Arial", 18))
        self.label.pack(pady=20)

        self.scrollbar = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(self.main_frame, yscrollcommand=self.scrollbar.set, font=("Arial", 12), width=100)
        self.listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.listbox.yview)

        conn = sqlite3.connect("students.db")
        c = conn.cursor()

        c.execute("SELECT * FROM students")
        students = c.fetchall()

        for student in students:
            student_id, name, roll_number, attendance, face_encoding_blob = student
            face_encoding = pickle.loads(face_encoding_blob)

     
            formatted_string = f"ID: {student_id:<5} Name: {name:<20} Roll Number: {roll_number:<10} Attendance: {attendance:<15}"
            self.listbox.insert(tk.END, formatted_string)

        c.close()
        conn.close()

        self.quit_button = util.get_button(self.main_frame, "Quit",'red', self.parent.quit)
        self.quit_button.pack(pady=10)
        self.quit_button.config(width = 10, height = 1)

if __name__ == "__main__":
    root = tk.Tk()
    controller = None
    app = AttendanceReportApp(root,controller)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
