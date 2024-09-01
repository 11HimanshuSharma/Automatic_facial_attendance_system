import tkinter as tk
from tkinter import Frame
import add_students
import util
import mode_select
import getreport  # Import the module where `AttendanceReportApp` is defined

class Teacher(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.parent = parent
        self.parent.title("Teacher's Portal")
        self.parent.geometry("900x480+350+100")

        self.main_frame = Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.label = tk.Label(self.main_frame, text="Welcome! to the teacher's portal", font=("Comic Sans MS", 30))
        self.label.grid(row=0, columnspan= 2,padx=50, pady=60)

        self.mode_selection_button = util.get_button(self.main_frame, "Select Mode", 'blue', self.mode_selection)
        self.mode_selection_button.grid(row=1, column=0, padx=60, pady=10, sticky="ew")
        
        self.add_students_button = util.get_button(self.main_frame, "Add New Students", 'green', self.add_students)
        self.add_students_button.grid(row=1, column=1, padx=60, pady=10, sticky="ew")
        
        self.student_report_button = util.get_button(self.main_frame, "Get Student Report", 'orange', self.get_report)
        self.student_report_button.grid(row=2, column=0, padx=60, pady=10, sticky="ew")
        
        self.close_button = util.get_button(self.main_frame, "Close", 'red', self.close)
        self.close_button.grid(row=2, column=1, padx=60, pady=10, sticky="ew")
        
        self.get_report_main_frame = None
        self.options_frame = None

    def get_report(self):
        self.main_frame.pack_forget()
        
        if self.get_report_main_frame:
            self.get_report_main_frame.pack()
        else:
            self.get_report_main_frame = getreport.AttendanceReportApp(self.parent, self)
            self.get_report_main_frame.pack(fill=tk.BOTH, expand=True)
        self.destroy()
        
    def close(self):
        self.parent.destroy()

    def add_students(self):
        self.show_frame(add_students.RegisterApp)
        
    def mode_selection(self):
        self.show_frame(mode_select.ModeSelection)

    def show_frame(self, FrameClass):
        self.main_frame.pack_forget()
        if self.options_frame:
            self.options_frame.pack_forget()
        
        self.options_frame = FrameClass(self.parent, self)
        self.options_frame.pack(fill=tk.BOTH, expand=True)
        self.destroy()
        
  

if __name__ == "__main__":
    root = tk.Tk()
    app = Teacher(root, None)
    app.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
