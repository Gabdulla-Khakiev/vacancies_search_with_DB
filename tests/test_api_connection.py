def test_api_connection(vacancy_from_hh):
    assert vacancy_from_hh.connect() == True


def test_load_vacancies(vacancy_from_hh):
    vacancy_from_hh.get_vacancies("developer")
    assert len(vacancy_from_hh.vacancies) != 0
