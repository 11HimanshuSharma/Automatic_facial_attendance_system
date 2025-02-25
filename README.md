<!-- @format -->

# Facial_Recognition_attendance_system-using-face_recognition-lib

numpy version : 1.26.4 <br> face_recognition: python -c "import
face_recognition; 1.2.3 dlib-19.24.99-cp312-cp312-win_amd64.whl cmake tool


## 📌 Project Overview
The **Facial Attendance System** is an AI-powered attendance tracking system that leverages **Face Recognition** technology to automate the process of marking attendance. The system captures images from a webcam, identifies faces using a Convolutional Neural Network (CNN)-based model, and records attendance data in a database. The system is built using **Python, OpenCV, TensorFlow, NumPy, Tkinter (GUI), and a database for storage**.

## 🎯 Features
- **Automatic Face Detection**: Uses OpenCV and a pre-trained face recognition model.
- **Real-time Attendance Marking**: Detects and identifies faces in real-time.
- **GUI Interface**: Developed using Tkinter for an interactive experience.
- **Attendance Logging**: Stores attendance records in a local database.
- **Easy Integration**: Can be integrated with external systems via API.
- **Secure and Fast**: Uses a machine learning model for accurate recognition.

---

## 🛠️ Technologies Used
- **Programming Language**: Python
- **Libraries & Frameworks**:
  - OpenCV (for face detection and image processing)
  - TensorFlow/Keras (for face recognition model)
  - NumPy & Pandas (for data processing)
  - Tkinter (for GUI)
- **Database**: SQLite/MySQL
- **Additional Tools**: Virtual Environment (venv)

---

## 🚀 Installation Guide

### 🔹 Prerequisites
Before you begin, ensure you have the following installed:
- **Python 3.x** (Recommended: Python 3.8 or later)
- **pip** (Python package manager)
- **Virtual Environment (venv)** (Optional but recommended)

### 🔹 Step-by-Step Setup
1. **Clone the Repository**:
   ```sh
   git clone https://github.com/yourusername/facial-attendance-system.git
   cd facial-attendance-system
   ```

2. **Create and Activate a Virtual Environment** (Recommended):
   - Windows:
     ```sh
     python -m venv venv
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```sh
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Required Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Download Pre-trained Model (if required)**:
   ```sh
   python download_model.py
   ```

5. **Run the Application**:
   ```sh
   python app.py
   ```

6. **Launch the GUI**:
   ```sh
   python gui.py
   ```

---

## 📸 How It Works
1. **Face Registration**:
   - Users must first register their face using the GUI.
   - The system captures multiple images of the user.
   - The images are stored in the dataset folder and linked with an ID.

2. **Face Recognition & Attendance**:
   - When a user appears in front of the camera, the system detects and recognizes the face.
   - If the face is found in the database, attendance is marked automatically.
   - The entry is logged with a timestamp.

3. **Viewing Attendance Records**:
   - Users/admins can view attendance records in the database.
   - Data can be exported as a CSV file.

---


---

## 🛠️ Troubleshooting
### 🔹 Common Issues & Fixes
1. **Module Not Found Error**:
   - Run `pip install -r requirements.txt` to ensure all dependencies are installed.

2. **Camera Not Detected**:
   - Ensure the webcam is connected and accessible.
   - Run `python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"` to check.

3. **Face Not Recognized**:
   - Make sure you have registered your face properly.
   - Try retraining the model using `python train_model.py`.

4. **Database Connection Issues**:
   - Verify the database file exists in the `database/` folder.
   - Check for correct SQLite or MySQL configurations in the `config.py` file.



## 🤝 Contributing
We welcome contributions! Follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit changes (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a **Pull Request**.

---

## 📧 Contact
For queries or support, reach out to:
- **Email**: himanshusharma5908@gmail.com

