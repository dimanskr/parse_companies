import os
from dotenv import load_dotenv

# ID компаний в сфере IT:
# "Т-Банк", "SberTech", "Яндекс Крауд", "Т1", "Bell Integrator"
# "VK", "МТС", "Яндекс", "Х5 Group", "Норникель"
DEFAULT_COMPANIES_ID = ['78638', '906557', '9498112', '4649269', '6189',
                        '15478', '3776', '1740', '4233', '740']

PARAM_EMPLOYERS = {"text": "",
                   "page": 0,
                   "per_page": 100,
                   "only_with_vacancies": "true",
                   "sort_by": "by_vacancies_open",
                   "locale": "RU"}

PARAM_VACANCIES = {"text": "",
                   "page": 0,
                   "per_page": 100,
                   "only_with_salary": "true",
                   "vacancy_search_order": "publication_time",
                   "locale": "RU",
                   "period": 14}

load_dotenv()

db_config = {
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT'),
    'dbname': os.getenv('POSTGRES_DB')
}
