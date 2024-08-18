from src.vacancy import Vacancy


def test_hh_init(hh_instance):
    assert hh_instance._headers == {'User-Agent': 'HH-User-Agent'}
    assert hh_instance._params == {'text': '', 'page': 0, 'per_page': 100}
    assert hh_instance._vacancies == []


def test_load_employers_id_name(hh_instance):
    employers_list = hh_instance.load_employers(['78638', '906557', '9498112', '4649269', '6189',
                                                 '15478', '3776', '1740', '4233', '740'])
    assert len(employers_list) == 10
    assert employers_list[0]['id'] == "78638"
    assert employers_list[0]['name'] == "Т-Банк"


def test_load_vacancies_return_vacancies_instances(hh_instance, real_employer):
    real_vacancies_list = hh_instance.load_vacancies([real_employer])
    assert all(isinstance(vacancy, Vacancy) for vacancy in real_vacancies_list)
