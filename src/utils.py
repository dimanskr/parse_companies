def salary_to_str(salary_from: int | None, salary_to: int | None) -> str:
    """
    Функция принимает минимальную и максимальную зарплату и возвращает строку
    в удобочитаемом виде
    :param salary_from: ЗП от
    :param salary_to: ЗП до
    :return: str
    """
    if not salary_from and not salary_to:
        return "зарплата не указана"

    if salary_from:
        sal_from = f" от {salary_from}"
    else:
        sal_from = ""

    if salary_to:
        sal_to = f" до {salary_to}"
    else:
        sal_to = ""

    return f"зарплата{sal_from}{sal_to} руб."