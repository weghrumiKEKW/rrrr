import sqlite3

DATABASE = "students.db"


def create_connection():
    """Verilənlər bazasına bağlantı yaradır."""
    return sqlite3.connect(DATABASE)


def add_student(student_name, score):
    """Yeni tələbə əlavə edir."""
    connection = create_connection()

    try:
        connection.execute(
            """
            INSERT INTO Students (StudentName, Score)
            VALUES (?, ?)
            """,
            (student_name, score)
        )
        connection.commit()
    finally:
        connection.close()


def get_students():
    """Bütün tələbələri qaytarır."""
    connection = create_connection()

    try:
        cursor = connection.execute(
            """
            SELECT StudentID, StudentName, Score
            FROM Students
            ORDER BY StudentID
            """
        )

        return [
            {
                "StudentID": row[0],
                "Name": row[1],
                "Score": row[2]
            }
            for row in cursor.fetchall()
        ]
    finally:
        connection.close()


def get_student(student_name):
    """Ada görə tələbələri axtarır."""
    connection = create_connection()

    try:
        cursor = connection.execute(
            """
            SELECT StudentID, StudentName, Score
            FROM Students
            WHERE StudentName LIKE ?
            ORDER BY StudentName
            """,
            (f"%{student_name}%",)
        )

        return [
            {
                "StudentID": row[0],
                "Name": row[1],
                "Score": row[2]
            }
            for row in cursor.fetchall()
        ]
    finally:
        connection.close()


def initialize_database():
    """Cədvəl mövcud deyilsə, yaradır."""
    connection = create_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS Students (
                StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
                StudentName TEXT NOT NULL,
                Score INTEGER NOT NULL CHECK (Score BETWEEN 0 AND 100)
            )
            """
        )
        connection.commit()
    finally:
        connection.close()


initialize_database()