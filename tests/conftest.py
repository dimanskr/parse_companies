import pytest
from src.api import HH
from src.dbmanager import DBManager
from src.employer import Employer
from src.vacancy import Vacancy


@pytest.fixture
def hh_instance():
    return HH()


@pytest.fixture
def vacancy_api_data():
    return {
        "id": "1",
        "name": "Test Vacancy",
        "url": "http://example.com",
        "snippet": {
            "requirement": "Test Requirement",
            "responsibility": "Test Responsibility"
        },
        "salary": {
            "from": 50000,
            "to": 100000,
            "currency": "RUR"
        }
    }


@pytest.fixture
def vacancy_instance():
    vacancy = Vacancy(
        vacancy_id="1",
        name="Test Vacancy",
        url="http://example.com",
        employer_id="2",
        requirement="Test Requirement",
        responsibility="Test Responsibility",
        salary_from=50000,
        salary_to=100000,
        currency="RUR"
    )
    return vacancy


@pytest.fixture
def employer_api_data():
    return {
        "id": "1",
        "name": "Test Employer",
        "alternate_url": "http://example.com",
        "area": {
            "name": "Test City"
        },
        "description": "Test Description",
        "site_url": "http://employer-site.com",
        "vacancies_url": "http://example.com/vacancies",
        "open_vacancies": 10
    }


@pytest.fixture
def employer_instance():
    employer = Employer(
        employer_id="1",
        name="Test Employer",
        alternate_url="http://example.com",
        city="Test City",
        description="Test Description",
        site_url="http://employer-site.com",
        vacancies_url="http://example.com/vacancies",
        open_vacancies=10
    )
    return employer


@pytest.fixture(scope="module")
def db_manager():
    db = DBManager(dbname="test_db", user="postgres", password="postgres", host="localhost", port=5432)
    db.create_database()
    db.create_table()
    yield db
    db.drop_database()


@pytest.fixture
def sample_data():
    employers = [
        Employer(employer_id="1", name="Company A", alternate_url="http://companya.com", city="City A",
                 description="A great company", site_url="http://site.com", vacancies_url="http://vacancies.com", open_vacancies=5),
        Employer(employer_id="2", name="Company B", alternate_url="http://companyb.com", city="City B",
                 description="Another great company", site_url="http://siteb.com", vacancies_url="http://vacanciesb.com", open_vacancies=3)
    ]
    vacancies = [
        Vacancy(vacancy_id="1", name="Python Developer", url="http://vacancy1.com", employer_id="1",
                requirement="Experience with Python", responsibility="Develop software", salary_from=100000, salary_to=150000, currency="RUB"),
        Vacancy(vacancy_id="2", name="Data Scientist", url="http://vacancy2.com", employer_id="2",
                requirement="Experience with ML", responsibility="Analyze data", salary_from=120000, salary_to=170000, currency="RUB"),
        Vacancy(vacancy_id="3", name="DevOps Engineer", url="http://vacancy3.com", employer_id="1",
                requirement="Experience with CI/CD", responsibility="Maintain infrastructure", salary_from=110000, salary_to=160000, currency="RUB")
    ]
    return employers, vacancies


@pytest.fixture
def setup_data(db_manager, sample_data):
    employers, vacancies = sample_data
    db_manager.clear_table()
    db_manager.insert_companies(employers)
    db_manager.insert_vacancies(vacancies)
