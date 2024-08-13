class Employer:
    """
    Класс работодатель HH.ru
    """
    __slots__ = (
        '__employer_id', '__name', '__alternate_url', '__city', '__description', '__site_url',
        '__vacancies_url', '__open_vacancies')

    def __init__(self, employer_id: str, name: str, alternate_url: str, city: str,
                 description: str, site_url: str, vacancies_url: str, open_vacancies: int):
        self.__employer_id = employer_id if employer_id else ""
        self.__name = name if name else ""
        self.__alternate_url = alternate_url if alternate_url else ""
        self.__city = city if city else ""
        self.__description = description if description else ""
        self.__site_url = site_url if site_url else ""
        self.__vacancies_url = vacancies_url if vacancies_url else ""
        self.__open_vacancies = open_vacancies if open_vacancies else 0

    @property
    def employer_id(self):
        return self.__employer_id

    @property
    def name(self):
        return self.__name

    @property
    def alternate_url(self):
        return self.__alternate_url

    @property
    def city(self):
        return self.__city

    @property
    def description(self):
        return self.__description

    @property
    def site_url(self):
        return self.__site_url

    @property
    def vacancies_url(self):
        return self.__vacancies_url

    @property
    def open_vacancies(self):
        return self.__open_vacancies

    def __str__(self) -> str:
        return (f"Компания '{self.__name}' с ID {self.__employer_id} \n"
                f"Описание: {self.__description}\n"
                f"Город: {self.__city}\n"
                f"Сайт компании: {self.__site_url}\n"
                f"Кол-во вакансий {self.__open_vacancies}\n"
                f"Ссылка на вакансии компании: {self.__alternate_url}\n")

    @classmethod
    def new_employer(cls, data: dict) -> 'Employer':
        """
        Метод создания экземпляра класса работодатель.
        :param data: Словарь данных компании, полученный при обращении к API
        :return: объект 'Employer'
        """
        employer_id = data.get("id", "")
        name = data.get("name", "")
        alternate_url = data.get("alternate_url", "")
        city = data.get("area", {}).get("name", "")
        description = data.get("description", "")
        site_url = data.get("site_url", "")
        vacancies_url = data.get("vacancies_url", "")
        open_vacancies = data.get("open_vacancies", 0)

        return cls(employer_id, name, alternate_url, city, description, site_url, vacancies_url, open_vacancies)

    @classmethod
    def cast_to_object_list(cls, data: list[dict]) -> list['Employer']:
        """
        Возвращает список экземпляров класса Employer
        :param data: список словарей объектов
        :return: employers_list список объектов 'Employer'
        """
        employers_list = []
        for emp in data:
            employer = cls.new_employer(emp)
            employers_list.append(employer)
        return employers_list
