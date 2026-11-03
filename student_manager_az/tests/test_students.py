import pytest

from student_manager_az.database.database import get_connection
from student_manager_az.services.students import (
    get_students,
    add_student,
    delete_student,
    search_students,
)


@pytest.fixture
def setup_database(tmp_path, monkeypatch):
    """Prépare une base SQLite temporaire pour les tests."""

    database_file = tmp_path / "test_students.db"

    def get_test_connection():
        import sqlite3
        return sqlite3.connect(database_file)

    monkeypatch.setattr(
        "student_manager_az.services.students.get_connection",
        get_test_connection,
    )


    with get_test_connection() as connection:
        connection.execute("""
            CREATE TABLE students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT,
                class_name TEXT
            )
        """)

    return database_file


def test_add_student(setup_database):
    """ vérifier l’ajout d’un étudiant """
    student_id = add_student(
        "Alice", "Martin", "alice@example.com", "BTS SIO"
    )

    assert student_id == 1


def test_get_students(setup_database):
    add_student(
        "Alice", "Martin", "alice@example.com", "BTS SIO"
    )

    student_list = get_students()

    assert len(student_list) == 1

def test_delete_student(setup_database):
    # À compléter : vérifier la suppression d’un étudiant.
    add_student(
        "Alice", "Martin", "alice@example.com", "BTS SIO"
    )
    delete_student(1)
    student_list = get_students()
    assert len(student_list) == 0

def test_search_students(setup_database):
    add_student("Pablo", "Escobar", "pablo@exemple.com", "BTS SIO")
    add_student("Escobar", "Pablo", "pablo2@exemple.com", "BTS SIO")
    add_student("Escobar", "PasPablo", "pablo3@exemple.com", "BTS SIO")

    student_list = search_students("Pablo")

    assert len(student_list) == 2

    first_names = [student[1] for student in student_list]
    last_names = [student[2] for student in student_list]

    assert "Pablo" in first_names
    assert "Pablo" in last_names

def test_search_students_no_result(setup_database):
    # À compléter : vérifier le comportement de la recherche lorsqu’aucun étudiant ne correspond au critère indiqué.
    student_list = search_students("Personne")
    assert len(student_list) == 0

