from src.utils import salary_to_str


def test_salary_to_str():
    assert salary_to_str(None, None) == "зарплата не указана"
    assert salary_to_str(50000, None) == "зарплата от 50000 руб."
    assert salary_to_str(None, 100000) == "зарплата до 100000 руб."
    assert salary_to_str(50000, 100000) == "зарплата от 50000 до 100000 руб."
    assert salary_to_str(0, 0) == "зарплата не указана"
