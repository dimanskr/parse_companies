from config import db_config, DEFAULT_COMPANIES_ID
from src.api import HH
from src.dbmanager import DBManager
from src.employer import Employer
from src.utils import salary_to_str


def download_data_from_api_to_db(db):
    """
    Функция загрузки данных с API и сохранение их в базу данных
    :param db: уккзатель на БД
    """

    # создаем объект парсера вакансий с HH.ru
    hh = HH()

    # выбираем работодателей через API из списка ID компаний
    print('\n Загрузка данных о компаниях через API')
    chosen_companies_list = hh.load_employers(DEFAULT_COMPANIES_ID)
    companies_object_list: list[Employer] = Employer.cast_to_object_list(chosen_companies_list)
    print('\nСписок компаний для поиска вакансий:')
    for company in companies_object_list:
        print(company.name, end=' ')
    print('\n Загрузка вакансий через API')
    chosen_vacancies_list = hh.load_vacancies(companies_object_list)

    # загружаем данные в БД
    print('\nЗагрузка компаний в БД')
    db.insert_companies(companies_object_list)
    print('Загрузка вакансий в БД')
    db.insert_vacancies(chosen_vacancies_list)


def user_interaction():
    """
        Функция для взаимодействия с пользователем и управления работой программы.

        Функция предоставляет пользователю меню с различными действиями, такими как:
        - Получение списка всех компаний и количества вакансий у каждой компании
        - Получение списка всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки
         на вакансию
        - Получение средней зарплаты по вакансиям.
        - Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям
        - Получение списка всех вакансий, в названии которых содержится ключевое слово
        - Удаление данных из базы данных если они там содержатся на момент начала работы программы или в ходе
        - Завершение программы

        Пользователь может выбирать действие, вводя соответствующий номер, и программа будет
        выполнять выбранное действие.
        """

    # создаем подключение к БД таблицы
    db = DBManager(**db_config)
    db.create_database()
    db.create_table()

    # если таблицы пустые, загружаем данные с API
    if not db.has_records('companies') and not db.has_records('vacancies'):
        download_data_from_api_to_db(db)
    else:
        # иначе предлагаем принудительно очистить или работать с имеющимися данными
        print('Таблицы БД заполнены данными.')
        print("Нажмите 1, чтобы очистить содержимое таблиц БД и получить "
              "новые данные от API,")
        print("или любое другое значение для работы с имеющимися данными")
        user_input = input()
        if user_input == "1":
            #  Очищаем таблицы БД, если они были созданы ранее
            db.clear_table()
            download_data_from_api_to_db(db)

    while True:
        print("\nВыберите действие:")
        print("1. Получить список всех компаний и количество вакансий у каждой компании.")
        print("2. Получить список всех вакансий с указанием названия компании, "
              "названия вакансии и зарплаты и ссылки на вакансию.")
        print("3. Получить среднюю зарплату по вакансиям.")
        print("4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям.")
        print("5. Получить список всех вакансий, в названии которых содержится ключевое слово.")
        print("6. Удалить данные из базы данных.")
        print("7. Завершить программу.")

        user_input = input("Введите номер действия: ")

        if user_input == "1":
            companies = db.get_companies_and_vacancies_count()
            for comp in companies:
                print(f"'{comp[0]}', кол-во вакансий {comp[1]}")
        elif user_input == "2":
            vacancies = db.get_all_vacancies()
            for vac in vacancies:
                print(f"'{vac[0]}', {vac[1]}, {salary_to_str(vac[2], vac[3])}, "
                      f"ссылка: {vac[4]}")
        elif user_input == "3":
            print(f"Средняя зарплата: {db.get_avg_salary()}")
        elif user_input == "4":
            avg_vacancies = db.get_vacancies_with_higher_salary()
            for avg_vac in avg_vacancies:
                print(f"'{avg_vac[0]}', {avg_vac[1]}, {salary_to_str(avg_vac[2], avg_vac[3])}, "
                      f"ссылка: {avg_vac[4]}")
        elif user_input == "5":
            search_query = input("Введите ключевое слово: ")
            vacancies_with_keyword = db.get_vacancies_with_keyword(search_query)
            for vac_with_kw in vacancies_with_keyword:
                print(f"'{vac_with_kw[0]}', {vac_with_kw[1]}, "
                      f"{salary_to_str(vac_with_kw[2], vac_with_kw[3])}, "
                      f"ссылка: {vac_with_kw[4]}")
        elif user_input == "6":
            db.clear_table()
            print("Таблицы очищены.")
        elif user_input == "7":
            print("Программа завершена.")
            break

        else:
            print("Некорректный ввод. Повторите попытку.")


if __name__ == "__main__":
    user_interaction()
