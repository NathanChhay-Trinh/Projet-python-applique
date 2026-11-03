from student_manager_az.database import get_connection

def get_student_count():
    with get_connection() as connection:
        return connection.execute(
            "SELECT COUNT(*) FROM students"
        ).fetchone()[0]


def get_general_average():
    with get_connection() as connection:
        result = connection.execute(
            "SELECT AVG(grade) FROM grades"
        ).fetchone()

        # Sans note dans la base, on renvoie 0.
        return result[0] if result[0] is not None else 0


def get_class_average(class_name):
    with get_connection() as connection:
        # On ne prend que les notes des étudiants de cette classe.
        result = connection.execute(
            """
            SELECT AVG(grades.grade)
            FROM grades
            JOIN students ON grades.student_id = students.id
            WHERE students.class_name = ?
            """,
            (class_name,),
        ).fetchone()

        return result[0] if result[0] is not None else 0