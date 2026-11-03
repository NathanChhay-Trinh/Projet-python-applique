import pytest
import sqlite3
from student_manager_az.database import database
from student_manager_az.services.grades import (
    add_grade,
    get_student_average,
    get_grades_by_student
)


@pytest.fixture
def setup_database(tmp_path, monkeypatch):
    """Prépare une base SQLite temporaire pour les tests."""

    database_file = tmp_path / "test_grades.db"

    monkeypatch.setattr(database, "DATABASE_NAME", str(database_file))
    database.init_database()
    with database.get_connection() as connection:
        connection.execute(
            "INSERT INTO students (first_name, last_name) VALUES (?, ?)",
            ("Alice", "Martin"),
        )

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
    assert grade_student == [(1, "Python", 20.0)]

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
