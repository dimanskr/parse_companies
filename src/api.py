import requests
from abc import ABC, abstractmethod

from config import PARAM_EMPLOYERS, PARAM_VACANCIES
from src.employer import Employer
from src.mixins import ProgressBarMixin
from src.vacancy import Vacancy


class Parser(ABC):

    @abstractmethod
    def load_employers(self, id_list: list[str]) -> list[dict]:
        """
        Абстрактный метод загрузки работодателей
        """
        pass

    @abstractmethod
    def load_vacancies(self, data: dict[int, str]) -> list:
        """
        Абстрактный метод для получения всех вакансий работодателя
        """
        pass


class HH(Parser, ProgressBarMixin):
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self):
        self._headers: dict = {"User-Agent": "HH-User-Agent"}
        self._params: dict = {"text": "", "page": 0, "per_page": 100}
        self._vacancies: list[dict] = []

    def load_employers(self, id_list: list[str]) -> list[dict]:
        """
        Метод загрузки выбранных пользователем компаний
        :param id_list: list[str] список ID компаний
        :return: list[dict]: Список с компаниями в формате JSON
        """
        if PARAM_EMPLOYERS:
            self._params = PARAM_EMPLOYERS
        employers_list: list[dict] = []
        for number, employer_id in enumerate(id_list):
            if self.show_progress(number, len(id_list)):
                self.show_progress(number, len(id_list))
            response = requests.get(f'https://api.hh.ru/employers/{employer_id}', params=self._params)
            if response.status_code == 200:
                data_employer = response.json()
                employers_list.append(data_employer)

        return employers_list

    def load_vacancies(self, employer_list: list[Employer]) -> list[Vacancy]:
        """
        Метод для получения всех вакансий работодателя
        [в тестовом виде показываем только 100 ближайших по дате вакансий работодателя]
        :param employer_list: список объектов работодателей
        :return: список объектов вакансий соответствующих списку работодателей
        """
        try:
            vacancies_data_list: list[Vacancy] = []
            if PARAM_VACANCIES:
                self._params = PARAM_VACANCIES

            for number, employer in enumerate(employer_list):
                if self.show_progress(number, len(employer_list)):
                    self.show_progress(number, len(employer_list))
                employer_id = employer.employer_id
                vacancies_url = employer.vacancies_url
                response = requests.get(vacancies_url, params=self._params)
                if response.status_code == 200:
                    vacancies: list[dict] = response.json()['items']
                    employer_vacancies: list[Vacancy] = Vacancy.cast_to_object_list(vacancies, employer_id)
                    vacancies_data_list.extend(employer_vacancies)
            return vacancies_data_list

        except requests.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return []
