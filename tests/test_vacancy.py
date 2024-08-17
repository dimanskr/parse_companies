from src.vacancy import Vacancy


def test_vacancy_init(vacancy_instance):
    vacancy = vacancy_instance

    assert vacancy.vacancy_id == "1"
    assert vacancy.name == "Test Vacancy"
    assert vacancy.url == "http://example.com"
    assert vacancy.employer_id == "2"
    assert vacancy.requirement == "Test Requirement"
    assert vacancy.responsibility == "Test Responsibility"
    assert vacancy.salary_from == 50000
    assert vacancy.salary_to == 100000
    assert vacancy.currency == "RUR"


def test_salary_both(vacancy_instance):
    vacancy = vacancy_instance
    assert vacancy.salary == "зарплата от 50000 до 100000 RUR."


def test_str(vacancy_instance):
    vacancy = vacancy_instance
    expected_str = (
        "Вакансия: Test Vacancy, ссылка: http://example.com \n"
        "зарплата от 50000 до 100000 RUR. \n"
        "Требования: Test Requirement \n"
        "Обязанности: Test Responsibility"
    )
    assert str(vacancy) == expected_str


def test_lt(vacancy_instance):

    vacancy2 = Vacancy(
        vacancy_id="v2",
        name="Vacancy 2",
        url="http://example.com",
        employer_id="e2",
        requirement="Requirement 2",
        responsibility="Responsibility 2",
        salary_from=60000,
        salary_to=110000,
        currency="RUR"
    )
    assert vacancy_instance < vacancy2


def test_eq(vacancy_instance):

    vacancy2 = Vacancy(
        vacancy_id="v2",
        name="Vacancy",
        url="http://example.com",
        employer_id="e1",
        requirement="Requirement",
        responsibility="Responsibility",
        salary_from=50000,
        salary_to=100000,
        currency="RUR"
    )
    assert vacancy_instance == vacancy2


def test_new_vacancy(vacancy_api_data, vacancy_instance):
    vacancy = Vacancy.new_vacancy(vacancy_api_data, employer_id="2")
    assert vacancy == vacancy_instance


def test_cast_to_object_list(vacancy_api_data):
    data = [vacancy_api_data, vacancy_api_data]  # Example with duplicate data
    employer_id = "2"
    vacancies = Vacancy.cast_to_object_list(data, employer_id)
    assert len(vacancies) == 2
    for vacancy in vacancies:
        assert vacancy.employer_id == employer_id
        assert vacancy.vacancy_id == "1"
        assert vacancy.name == "Test Vacancy"
        assert vacancy.url == "http://example.com"
        assert vacancy.requirement == "Test Requirement"
        assert vacancy.responsibility == "Test Responsibility"
        assert vacancy.salary_from == 50000
        assert vacancy.salary_to == 100000
        assert vacancy.currency == "RUR"
