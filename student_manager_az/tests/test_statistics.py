import pytest
import sqlite3
from student_manager_az.database.database import get_connection
from student_manager_az.services.statistics import (
get_student_count,
get_general_average,
get_class_average,
)
from student_manager_az.services.students import (
    get_students,
    add_student,
    delete_student,
    search_students,
)
from student_manager_az.services.grades import (
    add_grade,
    get_student_average,
    get_grades_by_student
)
from student_manager_az.services.students import (
    add_student,
)

@pytest.fixture
def setup_database(tmp_path, monkeypatch):
    """Prépare une base SQLite temporaire pour les tests."""

    database_file = tmp_path / "test_statistics.db"

    def get_test_connection():
        import sqlite3
        return sqlite3.connect(database_file)

    monkeypatch.setattr(
        "student_manager_az.services.statistics.get_connection",
        get_test_connection,
    )
    monkeypatch.setattr(
        "student_manager_az.services.students.get_connection",
        get_test_connection,
    )
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
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT,
                class_name TEXT
            )
            """
        )
        for i in range(5):
            add_student("Alice", "Au_pays_des_merveilles","alice@gmail.com","BTS SIO")
        for i in range(5):
            for j in range(5):
                add_grade(i+1, j+1, 15+i)

    return database_file

def test_get_student_count(setup_database):
    total_students = get_student_count()
    assert total_students == 5
def test_get_general_average(setup_database):
    avg_students= get_general_average()
    assert avg_students == 17

def test_get_class_average(setup_database):
    avg_students= get_class_average("BTS SIO")
    assert avg_students == 17

def test_get_class_average_without_grades(setup_database) :
    with sqlite3.connect(setup_database) as connection:
        connection.execute("""
            DELETE FROM grades
        """)
        avg_students= get_class_average("BTS SIO")
        assert avg_students == 0