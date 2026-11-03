import pytest
import sqlite3
from student_manager_az.database.database import get_connection
from student_manager_az.services.grades import (
    add_grade,
    get_student_average,
    get_grades_by_student
)


@pytest.fixture
def setup_database(tmp_path, monkeypatch):
    """Prépare une base SQLite temporaire pour les tests."""

    database_file = tmp_path / "test_grades.db"

    def get_test_connection():
        import sqlite3
        return sqlite3.connect(database_file)

    monkeypatch.setattr(
        "student_manager_az.services.grades.get_connection",
        get_test_connection,
    )

    with get_test_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                grade REAL NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (subject_id) REFERENCES subjects(id)
            )
        """)


    return database_file

def test_add_grade(setup_database):
    add_grade(1, 1, 20)
    with sqlite3.connect(setup_database) as connection:
        cursor = connection.execute("""SELECT * FROM grades WHERE student_id = 1""")
        grade = cursor.fetchone()
        assert grade[3] == 20

def  test_get_grades_by_student(setup_database) :
    add_grade(1, 1, 20)
    grade_student = get_grades_by_student(1)
    assert grade_student == 20

def test_get_student_average(setup_database) :
    add_grade(1, 1, 20)
    add_grade(1, 2, 10)
    add_grade(1, 3, 20)
    add_grade(1, 4, 15)
    add_grade(1, 5, 12)

    avg_grade = get_student_average(1)
    assert avg_grade == 15.4

def test_get_student_average_without_grades(setup_database) :
    zero_grade = get_student_average(1)
    assert zero_grade == 0