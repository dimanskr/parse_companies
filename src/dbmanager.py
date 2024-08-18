from abc import ABC, abstractmethod

import psycopg2

from src.employer import Employer
from src.vacancy import Vacancy


class AbstractDBManager(ABC):
    """
    Представляет абстрактный класс AbstractDBManager.
    """

    @abstractmethod
    def create_table(self):
        """
        Абстрактный метод для создания таблицы.
        """
        pass

    @abstractmethod
    def clear_table(self):
        """
        Абстрактный метод для очистки содержимого БД таблицы.
        """
        pass


class DBManager(AbstractDBManager):
    """
    Класс менеджера базы данных.
    """

    def __init__(self, dbname: str, user: str, password: str, host: str, port: int):
        self.__dbname = dbname
        self.__user = user
        self.__password = password
        self.__host = host
        self.__port = port
        self.__conn = psycopg2.connect(dbname='postgres', user=user, password=password,
                                       host=host, port=port)
        self.create_database()

    def create_database(self):
        # Подключение к существующей базе данных, например, postgres
        self.__conn.autocommit = True  # Включение режима autocommit для создания базы данных
        cursor = self.__conn.cursor()
        cursor.execute(f"""SELECT 1 FROM pg_database WHERE datname = '{self.__dbname}'""")
        exists = cursor.fetchone()
        if not exists:
            # Создание новой базы данных
            cursor.execute(f"""CREATE DATABASE {self.__dbname}""")
        # Закрытие подключения
        cursor.close()
        self.__conn.close()
        self.__conn = psycopg2.connect(dbname=self.__dbname, user=self.__user,
                                       password=self.__password, host=self.__host, port=self.__port)

    def create_table(self):
        with self.__conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS companies(
                id SERIAL PRIMARY KEY,
                employer_id VARCHAR(16),
                name VARCHAR(150) NOT NULL,
                alternate_url VARCHAR(255),
                city VARCHAR(100),
                description TEXT,
                site_url VARCHAR(255),
                vacancies_url VARCHAR(255) NOT NULL,
                open_vacancies INTEGER
            );
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies(
                id SERIAL PRIMARY KEY,
                vacancy_id VARCHAR(16),
                name VARCHAR(150) NOT NULL,
                url VARCHAR(255) NOT NULL,
                company_id INT,
                requirement TEXT,
                responsibility TEXT,
                salary_from INTEGER NULL,
                salary_to INTEGER NULL,
                currency VARCHAR(3),
                FOREIGN KEY (company_id) REFERENCES companies(id)
            );
            """)
        self.__conn.commit()

    def insert_companies(self, data: list[Employer]):
        """
        Заполняет таблицу данными о компаниях
        :param data: data(list[Employer]): список с объектами класса 'Employer'
        """
        with self.__conn.cursor() as cur:
            sql = """
            INSERT INTO companies (employer_id, name, alternate_url, city,
            description, site_url, vacancies_url, open_vacancies) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """
            for item in data:
                cur.execute(sql, (item.employer_id, item.name,
                                  item.alternate_url, item.city,
                                  item.description, item.site_url, item.vacancies_url, item.open_vacancies))
        self.__conn.commit()

    def insert_vacancies(self, data: list[Vacancy]):
        """
        Заполняет таблицу данными о вакансиях
        :param data: data(list[Vacancy]): список с объектами класса 'Vacancy'
        :return:
        """
        with self.__conn.cursor() as cur:
            sql = """
            INSERT INTO vacancies (vacancy_id, name, url, 
            company_id, 
            requirement, responsibility, salary_from, salary_to, currency) 
            VALUES (%s, %s, %s, 
            (SELECT id FROM companies WHERE employer_id = %s), 
            %s, %s, %s, %s, %s);
            """
            for item in data:
                cur.execute(sql, (item.vacancy_id, item.name,
                                  item.url, item.employer_id,
                                  item.requirement, item.responsibility,
                                  item.salary_from, item.salary_to,
                                  item.currency))
        self.__conn.commit()

    def clear_table(self):
        """
        Очищает таблицу, если она существует.
        """
        with self.__conn.cursor() as cur:
            cur.execute(f"""
                TRUNCATE TABLE companies, vacancies RESTART IDENTITY CASCADE;
               """)
        self.__conn.commit()

    def has_records(self, table_name):
        """
        Проверяет, есть ли хотя бы одна запись в указанной таблице
        :param table_name: Имя таблицы для проверки
        :return: True, если есть хотя бы одна запись, иначе False
        """
        with self.__conn.cursor() as cur:
            cur.execute(f"SELECT EXISTS(SELECT 1 FROM {table_name} LIMIT 1);")
            return cur.fetchone()[0]

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        :return: list[tuple[]: список всех компаний и количество вакансий у каждой компании.
        """
        with self.__conn.cursor() as cur:
            cur.execute("""
                    SELECT companies.name, COUNT(vacancies.id)
                    FROM companies
                    LEFT JOIN vacancies ON companies.id = vacancies.company_id
                    GROUP BY companies.name;
                """)
            results: list[tuple] = cur.fetchall()
        self.__conn.commit()

        return results

    def get_all_vacancies(self) -> list[tuple]:
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии
        и зарплаты и ссылки на вакансию.
        :return: list[tuple]: список всех вакансий с указанием названия компании, названия вакансии
        и зарплаты и ссылки на вакансию.
        """
        with self.__conn.cursor() as cur:
            cur.execute("""
                    SELECT comp.name, vac.name, vac.salary_from, vac.salary_to, vac.url
                    FROM vacancies as vac
                    JOIN companies as comp ON vac.company_id = comp.id;
                """)
            results: list[tuple] = cur.fetchall()

        self.__conn.commit()

        return results

    def get_avg_salary(self) -> float:
        """
        Получает среднюю зарплату по вакансиям.
        :return: float: Средняя зарплата по вакансиям.
        """
        with self.__conn.cursor() as cur:
            cur.execute("""
                SELECT AVG((salary_from + salary_to) / 2.0) AS avg_salary
                FROM vacancies
                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL;
            """)

            result: tuple | None = cur.fetchone()
            avg_salary = result[0] if result[0] is not None else 0.0

        self.__conn.commit()

        return round(avg_salary, 2)

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        :return: list[tuple]: Список вакансий с зарплатой выше средней.
        """
        with self.__conn.cursor() as cur:
            # Первый запрос: получаем среднюю зарплату
            cur.execute("""
                SELECT AVG((salary_from + salary_to) / 2.0) AS avg_salary
                FROM vacancies
                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL;
            """)

            result: tuple | None = cur.fetchone()
            avg_salary = result[0] if result[0] is not None else 0.0

            # Второй запрос: получаем вакансии с зарплатой выше средней
            cur.execute(f"""
                SELECT comp.name, vac.name, vac.salary_from, vac.salary_to, vac.url
                FROM vacancies as vac
                JOIN companies as comp ON vac.company_id = comp.id
                WHERE (vac.salary_from + vac.salary_to) / 2.0 > {avg_salary};
            """)

            vacancies_data: list[tuple] = cur.fetchall()

        self.__conn.commit()

        return vacancies_data

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple]:
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например, python.
        :param keyword: (str) переданное в запрос слово
        :return: list[tuple]: список всех вакансий, в названии которых содержатся переданные в метод слова.
        """
        with self.__conn.cursor() as cur:
            # Используем параметризацию для безопасности
            cur.execute("""
                SELECT comp.name, vac.name, vac.salary_from, vac.salary_to, vac.url
                FROM vacancies AS vac
                JOIN companies AS comp ON vac.company_id = comp.id
                WHERE vac.name LIKE %s;
            """, (f'%{keyword}%',))

            vacancies_data: list[tuple] = cur.fetchall()

        self.__conn.commit()

        return vacancies_data

    def drop_database(self):
        """
        Удаляет базу данных, если она существует.
        """
        # Закрываем текущее соединение
        self.__conn.close()

        # Создаем новое соединение с базой данных postgres
        self.__conn = psycopg2.connect(dbname="postgres", user=self.__user,
                                       password=self.__password, host=self.__host, port=self.__port)
        self.__conn.autocommit = True
        cursor = self.__conn.cursor()

        # Закрываем все активные соединения с удаляемой базой данных
        cursor.execute(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{self.__dbname}'
              AND pid <> pg_backend_pid();
        """)

        # Удаляем базу данных
        cursor.execute(f"""DROP DATABASE IF EXISTS {self.__dbname};""")

        # Закрываем курсор и соединение
        cursor.close()
        self.__conn.close()

