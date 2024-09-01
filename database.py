import sqlite3
import pickle

def initialize_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students (
                 id INTEGER PRIMARY KEY,
                 name TEXT,
                 roll_number TEXT,
                 attendance INTEGER DEFAULT 0,
                 face_encoding BLOB)''')
    conn.commit()
    conn.close()
    

def add_student(name, roll_number, face_encoding):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()

 
    cur.execute("SELECT id FROM students WHERE roll_number = ?", (roll_number,))
    existing_student = cur.fetchone()

    if existing_student is None:
 
        face_encoding_blob = pickle.dumps(face_encoding)
        cur.execute("INSERT INTO students (name, roll_number, attendance, face_encoding) VALUES (?, ?, ?, ?)",
                    (name, roll_number, 0, face_encoding_blob))
    else:
        print("Student with roll number {} already exists.".format(roll_number))

    conn.commit()
    conn.close()


def get_all_students():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, roll_number, attendance, face_encoding FROM students')
    students = cursor.fetchall()
    conn.close()
    return students

def get_attendance(student_id):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('SELECT attendance FROM students WHERE id = ?', (student_id,))

    Attendance = cursor.fetchall()
    conn.close()
    return Attendance

def mark_attendance(student_id):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE students SET attendance = attendance + 1 WHERE id = ?', (student_id,))
    conn.commit()
    conn.close()


def know_face_encodings():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    
    c.execute("SELECT * FROM students")
    students = c.fetchall()
    
    known_face_encodings = []
    known_face_metadata = [] 
    
    for student in students:
        student_id, name, roll_number, attendance, face_encoding_blob = student
        face_encoding = pickle.loads(face_encoding_blob)[0]
        known_face_encodings.append(face_encoding) 
        known_face_metadata.append({
            "student_id": student_id,
            "name": name,
            "attendance": attendance,
            "roll_number": roll_number
        })
    
    conn.close()
    return known_face_encodings, known_face_metadata


def get_student_data_by_id(student_id):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    

    c.execute("SELECT * FROM students WHERE id=?", (student_id,))
    student = c.fetchone()
    
 
    if student:
        student_id, name, roll_number, attendance, face_encoding_blob = student
        student_data = {
            "student_id": student_id,
            "name": name,
            "roll_number": roll_number,
            "attendance": attendance
        }
    else:
        student_data = None  
    
    conn.close()
    return student_data

# # Example Usage
# initialize_db()
# # add_student('John Doe', '001', face_encoding)  # face_encoding should be provided
# students = get_all_students()
# print(students)
# known_face_encodings, known_face_metadata = know_face_encodings()
# print(known_face_metadata)
