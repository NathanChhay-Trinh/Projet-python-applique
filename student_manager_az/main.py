from student_manager_az.database import init_database
from student_manager_az.ui import create_main_window


def main():
    """
    Point d'entrée de l'application.
    """

    init_database()
    create_main_window()


if __name__ == "__main__":
    main()
