import pytest
import sqlite3
from student_manager_az.database.database import get_connection
from student_manager_az.services.subjects import (
    get_subjects
)

@pytest.fixture
def setup_database(tmp_path, monkeypatch):
    """Prépare une base SQLite temporaire pour les tests."""

    database_file = tmp_path / "test_subjects.db"

    def get_test_connection():
        import sqlite3
        return sqlite3.connect(database_file)

    monkeypatch.setattr(
        "student_manager_az.services.subjects.get_connection",
        get_test_connection,
    )

    with get_test_connection() as connection:
        connection.execute("""
                CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE)
        """)
        subjects = [
            ("Python",),
            ("SQL",),
            ("Réseaux",),
            ("Systèmes",),
            ("Web",)
        ]

        connection.executemany(
            """
            INSERT OR IGNORE INTO subjects (name)
            VALUES (?)
            """,
            subjects
        )

    return database_file


def  test_get_subjects(setup_database):
    subjects_list = get_subjects()
    assert len(subjects_list) == 5

def test_get_subjects_empty(setup_database):
    with sqlite3.connect(setup_database) as connection:
        connection.execute("DELETE FROM subjects")
    subjects_list = get_subjects()
    assert len(subjects_list) == 0