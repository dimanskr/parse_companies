from src.employer import Employer


def test_employer_init(employer_instance):
    employer = employer_instance
    assert employer.employer_id == "1"
    assert employer.name == "Test Employer"
    assert employer.alternate_url == "http://example.com"
    assert employer.city == "Test City"
    assert employer.description == "Test Description"
    assert employer.site_url == "http://employer-site.com"
    assert employer.vacancies_url == "http://example.com/vacancies"
    assert employer.open_vacancies == 10


def test_str(employer_instance):
    employer = employer_instance
    expected_str = (
        "Компания 'Test Employer' с ID 1 \n"
        "Описание: Test Description\n"
        "Город: Test City\n"
        "Сайт компании: http://employer-site.com\n"
        "Кол-во вакансий 10\n"
        "Ссылка на вакансии компании: http://example.com\n"
    )
    assert str(employer) == expected_str


def test_new_employer(employer_api_data):
    employer = Employer.new_employer(employer_api_data)
    assert employer.employer_id == "1"
    assert employer.name == "Test Employer"
    assert employer.alternate_url == "http://example.com"
    assert employer.city == "Test City"
    assert employer.description == "Test Description"
    assert employer.site_url == "http://employer-site.com"
    assert employer.vacancies_url == "http://example.com/vacancies"
    assert employer.open_vacancies == 10


def test_cast_to_object_list(employer_api_data):
    data = [employer_api_data, employer_api_data]  # Example with duplicate data
    employers = Employer.cast_to_object_list(data)
    assert len(employers) == 2
    for employer in employers:
        assert employer.employer_id == "1"
        assert employer.name == "Test Employer"
        assert employer.alternate_url == "http://example.com"
        assert employer.city == "Test City"
        assert employer.description == "Test Description"
        assert employer.site_url == "http://employer-site.com"
        assert employer.vacancies_url == "http://example.com/vacancies"
        assert employer.open_vacancies == 10
