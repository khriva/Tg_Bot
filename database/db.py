import sqlite3
import random
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "data", "school.db")

# создаём папку, если нет
os.makedirs(os.path.dirname(DB_NAME), exist_ok=True)

conn = sqlite3.connect(DB_NAME)
def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    #Создание таблицы учителей
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id INTEGER PRIMARY KEY AUTOINCREMENT  ,
            telegram_id INTEGER UNIQUE,
            full_name TEXT ,
            reserved_status BOOLEAN DEFAULT 0
        )
        """)

    # Создание таблицы учеников
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        telegram_id INTEGER UNIQUE,
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT ,
        teacher_id INTEGER,
        FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE CASCADE
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS homework (
    teacher_id FOREIGN KEY,
    student_id FOREIGN KEY,
    hw_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hw_date_created DATE DEFAULT CURRENT_DATE,
    hw_text TEXT,
    deadline_dateDATE,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
    
    )""")

    conn.commit()
    conn.close()


def add_student(telegram_id, full_name, teacher_id,student_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    conn.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
    INSERT INTO students (telegram_id, full_name, teacher_id,student_id)
    VALUES (?, ?, ?, ?)
    """, (telegram_id, full_name, teacher_id,student_id))

    conn.commit()
    conn.close()
def get_all_students():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()
    return students
def get_all_teachers():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT full_name FROM teachers")
    teachers = [t[0] for t in cursor.fetchall()]

    conn.close()
    return teachers

def generate_student_id():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    while True:
        new_id = random.randint(10000, 99999)

        cursor.execute("SELECT 1 FROM students WHERE student_id = ?", (new_id,))
        if not cursor.fetchone():
            break

    conn.close()
    return new_id
def get_teacher_by_id(teacher_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT full_name FROM teachers WHERE teacher_id = ?", (teacher_id,)
                   )
    teacher = cursor.fetchone()
    conn.close()
    if teacher :
        return teacher[0]
    return

def reserve_teacher_id(teacher_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(""" INSERT INTO teachers (teacher_id,reserved_status)
    VALUES (?, 0)""",(teacher_id,))
    conn.commit()
    conn.close()


def occupy_teacher_id(teacher_id, full_name, telegram_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT teacher_id FROM teachers WHERE teacher_id = ?", (teacher_id,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        return("Такого Id не существует ❌")
    if row["reserved_status"]:
        conn.close()
        return("Этот Id занят ❌")
    cursor.execute("""UPDATE teachers
        SET full_name = ?, telegram_id = ?, reserved_status = 1 
        WHERE teacher_id = ?
        """,(full_name,telegram_id,teacher_id)
                   )
    conn.commit()
    conn.close()
    return "Учитель успешно зарегистрирован ✅"
def show_students(teacher_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT full_name,student_id FROM students WHERE tg_id = ?", (teacher_id,))
    row = cursor.fetchone()
    return row

