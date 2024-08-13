from src.mixins import CleanTagsMixin


class Vacancy(CleanTagsMixin):
    """
    Класс вакансии с HH.ru
    """
    __slots__ = (
        '__vacancy_id', '__name', '__url', '__employer_id', '__requirement', '__responsibility',
        '__salary_from', '__salary_to', '__currency')

    def __init__(self, vacancy_id: str, name: str, url: str, employer_id: str, requirement: str,
                 responsibility: str, salary_from, salary_to, currency):
        self.__vacancy_id = vacancy_id if vacancy_id else ""
        self.__name = name if name else ""
        self.__url = url if url else ""
        self.__employer_id = employer_id
        self.__requirement = self.clean_tags(requirement) if requirement else ""
        self.__responsibility = self.clean_tags(responsibility) if responsibility else ""
        self.__salary_from = salary_from
        self.__salary_to = salary_to
        self.__currency = currency

    @property
    def vacancy_id(self):
        return self.__vacancy_id

    @property
    def name(self):
        return self.__name

    @property
    def url(self):
        return self.__url

    @property
    def employer_id(self):
        return self.__employer_id

    @property
    def requirement(self):
        return self.__requirement if self.__requirement else 'не указаны'

    @property
    def responsibility(self):
        return self.__responsibility if self.__responsibility else 'не указаны'

    @property
    def currency(self) -> str:
        return self.__currency

    @property
    def salary(self) -> str:
        """
        Метод вывода строки диапазона зарплат в формате: 1000 - 100000 RUR
        :return: str
        """
        if not self.__currency:
            return "зарплата не указана"

        if self.salary_from:
            sal_from = f" от {self.salary_from}"
        else:
            sal_from = ""

        if self.salary_to:
            sal_to = f" до {self.salary_to}"
        else:
            sal_to = ""

        return f"зарплата{sal_from}{sal_to} {self.currency}."

    @property
    def salary_from(self) -> int | None:
        """
        Нижняя граница зарплаты
        :return: int | None
        """
        return self.__salary_from

    @property
    def salary_to(self) -> int | None:
        """
        Верхняя граница зарплаты
        :return: int | None
        """
        return self.__salary_to

    def __str__(self):
        return (f"Вакансия: {self.__name}, ссылка: {self.__url} \n"
                f"{self.salary} \n"
                f"Требования: {self.requirement} \n"
                f"Обязанности: {self.responsibility}")

    def __lt__(self, other):
        # сравниваем верхний порог зарплат при наличии
        if self.salary_to and other.salary_to:
            return self.salary_to < other.salary_to
        # сравниваем верхний порог зарплат с нижним при наличии
        elif self.salary_to and other.salary_from:
            return self.salary_to < other.salary_from
        # если первое значение отсутствует, то оно автоматически меньше
        elif self.salary_to is None and other.salary_to:
            return True
        # сравниваем нижний порог зарплат при наличии
        elif self.salary_from and other.salary_from:
            return self.salary_from < other.salary_from
        # если первое значение отсутствует, то оно автоматически меньше
        elif self.salary_from is None and other.salary_from:
            return True

    def __eq__(self, other):
        # если верхние пороги зарплат равны
        if self.salary_to == other.salary_to:
            return True
        # верхних порогов зарплат нет, тогда сравниваем нижние
        elif self.salary_from is None and other.salary_from is None:
            return self.salary_from == other.salary_from
        # если нет данных по зарплатам, тогда они равны
        elif not self.__currency:
            return self.salary_from == other.salary_form

    @classmethod
    def new_vacancy(cls, data: dict, employer_id: str) -> 'Vacancy':
        """
        Метод для создания экземпляра класса Вакансия
        :param data: данные по вакансии
        :param employer_id: ID компании
        :return: Vacancy: экземпляр класса 'Vacancy'
        """
        salary_data = data.get('salary', {})

        vacancy_id = data.get("id", "")
        name = data.get("name", "")
        url = data.get("url", "")
        employer_id = employer_id
        requirement = data.get("snippet", {}).get("requirement", "")
        responsibility = data.get("snippet", {}).get("responsibility", "")
        salary_from = salary_data.get('from')
        salary_to = salary_data.get('to')
        currency = salary_data.get('currency')

        return cls(vacancy_id, name, url, employer_id, requirement, responsibility, salary_from,
                   salary_to, currency)

    @classmethod
    def cast_to_object_list(cls, data: list[dict], employer_id: str) -> list['Vacancy']:
        """
        Возвращает список экземпляров класса 'Vacancy'
        :param data: список словарей объектов
        :param employer_id: ID компании
        :return: employers_list список объектов 'Vacancy'
        """
        vacancies_list = []
        for vac in data:
            vacancy = cls.new_vacancy(vac, employer_id)
            vacancies_list.append(vacancy)
        return vacancies_list
