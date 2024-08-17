def test_get_companies_and_vacancies_count(db_manager, setup_data):
    result = db_manager.get_companies_and_vacancies_count()
    assert result == [("Company A", 2), ("Company B", 1)], (f"Expected [('Company A', 2), ('Company B', 1)], "
                                                            f"got {result}")


def test_get_all_vacancies(db_manager, setup_data):
    result = db_manager.get_all_vacancies()
    expected = [
        ("Company A", "Python Developer", 100000, 150000, "http://vacancy1.com"),
        ("Company B", "Data Scientist", 120000, 170000, "http://vacancy2.com"),
        ("Company A", "DevOps Engineer", 110000, 160000, "http://vacancy3.com")
    ]
    assert result == expected, f"Expected {expected}, got {result}"


def test_get_avg_salary(db_manager, setup_data):
    result = db_manager.get_avg_salary()
    expected_avg_salary = round((100000 + 150000) / 2 + (120000 + 170000) / 2 + (110000 + 160000) / 2, 2) / 3
    assert result == expected_avg_salary, f"Expected {expected_avg_salary}, got {result}"


def test_get_vacancies_with_higher_salary(db_manager, setup_data):
    result = db_manager.get_vacancies_with_higher_salary()
    expected = [
        ("Company B", "Data Scientist", 120000, 170000, "http://vacancy2.com")
    ]
    assert result == expected, f"Expected {expected}, got {result}"


def test_get_vacancies_with_keyword(db_manager, setup_data):
    result = db_manager.get_vacancies_with_keyword("Python")
    expected = [
        ("Company A", "Python Developer", 100000, 150000, "http://vacancy1.com")
    ]
    assert result == expected, f"Expected {expected}, got {result}"


def test_has_records(db_manager, setup_data):
    # Проверка, что таблица companies содержит записи
    assert db_manager.has_records("companies") is True, "Expected True, got False for companies table"
    # Проверка, что таблица vacancies содержит записи
    assert db_manager.has_records("vacancies") is True, "Expected True, got False for vacancies table"
    # Очищаем таблицу и проверяем снова
    db_manager.clear_table()
    # Проверка, что таблица companies не содержит записей после очистки
    assert db_manager.has_records("companies") is False, "Expected False, got True for companies table after clearing"
    # Проверка, что таблица vacancies не содержит записей после очистки
    assert db_manager.has_records("vacancies") is False, "Expected False, got True for vacancies table after clearing"



