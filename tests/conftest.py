import pytest

from src.api_connection import LoadVacancies
from src.vacancy import Vacancy


@pytest.fixture
def vacancy_from_hh():
    return LoadVacancies()
