import tkinter as tk
import util
from process_photo import FaceScannerApp as FaceScannerPhoto
from process_video import FaceScannerApp as FaceScannerVideo
from process_webcam import FaceScannerApp as FaceScannerWebcam

class ModeSelection(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        
        self.parent = parent
        self.parent.title("Mode Selection")
        self.parent.geometry("1200x520+350+100")
        
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.label = tk.Label(self.main_frame, text="Please select the Mode of Attendance", font=("Comic Sans MS", 30))
        self.label.pack(pady=20)
        
        self.create_buttons()
        self.mode_frame = None
    
    def create_buttons(self):
        button_texts = ['From photo', 'From video', 'From webcam']
        
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=70)
        
        self.image_process_button = util.get_button(button_frame, button_texts[0], 'blue', lambda: self.launch_subprocess(FaceScannerPhoto))
        self.image_process_button.grid(row=0, column=0, padx=9, pady=12)
        self.image_process_button.config(width=22)
        
        self.video_process_button = util.get_button(button_frame, button_texts[1], 'blue', lambda: self.launch_subprocess(FaceScannerVideo))
        self.video_process_button.grid(row=0, column=1, padx=10, pady=12)
        self.video_process_button.config(width=22)
        
        self.webcam_process_button = util.get_button(button_frame, button_texts[2], 'blue', lambda: self.launch_subprocess(FaceScannerWebcam))
        self.webcam_process_button.grid(row=0, column=2, padx=10, pady=12)
        self.webcam_process_button.config(width=22)
        
        self.close_button = util.get_button(self.main_frame, "Close", "red", self.close)
        self.close_button.pack(pady=10)
        self.close_button.config(width=70)
        
        
    def launch_subprocess(self, AppClass):
        self.main_frame.pack_forget()
        self.mode_frame = AppClass(self.parent, self)
        self.mode_frame.pack(fill=tk.BOTH, expand=True)
        self.destroy()
    
    def start(self):
        self.parent.mainloop()
        
    def close(self):
        self.parent.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    mode_selection = ModeSelection(root)
    mode_selection.pack(fill=tk.BOTH, expand=True)
    mode_selection.start()
