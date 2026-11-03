import pytest

from student_manager_az.database import database
from student_manager_az.services.grades import add_grade
from student_manager_az.services.students import add_student
from student_manager_az.services.statistics import (
    get_student_count,
    get_general_average,
    get_class_average,
)


@pytest.fixture
def setup_database(tmp_path, monkeypatch):
    database_file = tmp_path / "statistics.db"
    monkeypatch.setattr(database, "DATABASE_NAME", str(database_file))
    database.init_database()

    alice = add_student("Alice", "Martin", "", "B2")
    bob = add_student("Bob", "Dupont", "", "B1")

    # Clara nous sert à tester une classe sans notes.
    add_student("Clara", "Bernard", "", "B3")

    with database.get_connection() as connection:
        subject_id = connection.execute(
            "SELECT id FROM subjects WHERE name = 'Python'"
        ).fetchone()[0]

    add_grade(alice, subject_id, 12)
    add_grade(alice, subject_id, 18)
    add_grade(bob, subject_id, 6)

    return database_file


def test_get_student_count(setup_database):
    assert get_student_count() == 3


def test_get_general_average(setup_database):
    # (12 + 18 + 6) / 3 = 12.
    assert get_general_average() == pytest.approx(12)


def test_get_class_average(setup_database):
    assert get_class_average("B2") == pytest.approx(15)
    assert get_class_average("B1") == pytest.approx(6)


def test_get_class_average_without_grades(setup_database):
    assert get_class_average("B3") == 0