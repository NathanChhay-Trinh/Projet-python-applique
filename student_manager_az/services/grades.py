from student_manager_az.database import get_connection
import math



def add_grade(student_id, subject_id, grade):
    # La saisie peut arriver sous forme de texte depuis l'interface.
    try:
        grade = float(grade)
    except (TypeError, ValueError):
        raise ValueError("La note doit être un nombre.") from None

    if not math.isfinite(grade) or not 0 <= grade <= 20:
        raise ValueError("La note doit être comprise entre 0 et 20.")

    with get_connection() as connection:
        # On vérifie les deux ids avant d'enregistrer la note.
        student = connection.execute(
            "SELECT id FROM students WHERE id = ?",
            (student_id,),
        ).fetchone()

        if student is None:
            raise ValueError("Étudiant introuvable.")

        subject = connection.execute(
            "SELECT id FROM subjects WHERE id = ?",
            (subject_id,),
        ).fetchone()

        if subject is None:
            raise ValueError("Matière introuvable.")

        cursor = connection.execute(
            """
            INSERT INTO grades (student_id, subject_id, grade)
            VALUES (?, ?, ?)
            """,
            (student_id, subject_id, grade),
        )
        return cursor.lastrowid


def get_grades_by_student(student_id):
    with get_connection() as connection:
        # La jointure permet d'afficher le nom de la matière.
        return connection.execute(
            """
            SELECT grades.id, subjects.name, grades.grade
            FROM grades
            JOIN subjects ON grades.subject_id = subjects.id
            WHERE grades.student_id = ?
            ORDER BY grades.id
            """,
            (student_id,),
        ).fetchall()


def get_student_average(student_id):
    with get_connection() as connection:
        result = connection.execute(
            "SELECT AVG(grade) FROM grades WHERE student_id = ?",
            (student_id,),
        ).fetchone()

        # On garde 0 si l'étudiant n'a pas encore de note.
        return result[0] if result[0] is not None else 0