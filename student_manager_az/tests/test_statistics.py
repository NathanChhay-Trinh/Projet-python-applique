import pytest
from student_manager_az.services.statistics import (
get_student_count,
get_general_average,
get_class_average,
)

@pytest.fixture
def setup_database(tmp_path, monkeypatch):





    return database_file

def test_get_student_count(setup_database):
def test_get_general_average(setup_database):

def test_get_class_average(setup_database):

def test_get_class_average_without_grades(setup_database) :