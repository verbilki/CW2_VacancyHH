import pytest

from src.vacancy import Vacancy


def test_cast_to_object_list_skips_vacancy_with_missing_snippet_fields() -> None:
    """
    Test that cast_to_object_list skips a vacancy with missing 'responsibility' and 'requirement' fields in 'snippet'
    and continues processing others.

    This test ensures that when a vacancy dictionary is missing both 'responsibility' and 'requirement' fields
    in the 'snippet', it is skipped, and the method continues processing other valid vacancies.
    """
    hh_vacancies = [
        {
            "id": "123",
            "name": "Software Engineer",
            "alternate_url": "http://example.com/1",
            "snippet": {"requirement": "Requirement 1", "responsibility": "Responsibility 1"},
            "salary": {"from": 50000, "to": 70000},
        },
        {
            "id": "124",
            "name": "Data Scientist",
            "alternate_url": "http://example.com/2",
            # Missing 'responsibility' and 'requirement' fields
            "snippet": {},
            "salary": {"from": 60000, "to": 80000},
        },
        {
            "id": "125",
            "name": "Product Manager",
            "alternate_url": "http://example.com/3",
            "snippet": {"requirement": "Requirement 3", "responsibility": "Responsibility 3"},
            "salary": {"from": 55000, "to": 75000},
        },
    ]

    vacancies = Vacancy.cast_to_object_list(hh_vacancies)

    assert len(vacancies) == 3
    assert vacancies[0].vacancy_id == "123"
    assert vacancies[0].name == "Software Engineer"
    assert vacancies[1].vacancy_id == "124"
    assert vacancies[1].name == "Data Scientist"


def test_vacancy_init_raises_exception_on_empty_vacancy_id() -> None:
    """
    Test that initializing a Vacancy with an empty vacancy_id raises a ValueError.

    This test ensures that the Vacancy constructor raises a ValueError when
    the vacancy_id is provided as an empty string. The expected exception message
    is 'Invalid id'.
    """
    with pytest.raises(ValueError, match="Invalid id"):
        Vacancy(
            vacancy_id="",
            name="Software Engineer",
            url="http://example.com",
            description="Job description",
            salary=50000,
        )


def test_vacancy_init_raises_exception_on_special_characters_in_vacancy_id() -> None:
    """
    Test that initializing a Vacancy with a vacancy_id containing special characters raises a ValueError.

    This test ensures that the Vacancy constructor raises a ValueError when
    the vacancy_id is provided with special characters. The expected exception
    message is 'Invalid id'.
    """
    with pytest.raises(ValueError, match="Invalid id"):
        Vacancy(
            vacancy_id="123$%",
            name="Software Engineer",
            url="http://example.com",
            description="Job description",
            salary=50000,
        )


def test_vacancy_init_raises_exception_on_empty_name() -> None:
    """
    Test that initializing a Vacancy with an empty name raises a ValueError.

    This test ensures that the Vacancy constructor raises a ValueError when
    the name is provided as an empty string. The expected exception message is
    'Invalid name'.
    """
    with pytest.raises(ValueError, match="Invalid name"):
        Vacancy(vacancy_id="123", name="", url="http://example.com", description="Job description", salary=50000)


def test_vacancy_init_raises_exception_on_invalid_url() -> None:
    """
    Test that initializing a Vacancy with an invalid URL raises a ValueError.

    This test ensures that the Vacancy constructor raises a ValueError when
    the URL is not a valid HTTP URL. The expected exception message is 'Invalid URL'.

    Parameters:
    url (str): The URL to test for validity.

    Returns: None
    """
    with pytest.raises(ValueError, match="Invalid URL"):
        Vacancy(
            vacancy_id="123",
            name="Software Engineer",
            url="ftp://example.com",
            description="Job description",
            salary=50000,
        )


def test_vacancy_init_raises_exception_on_non_integer_salary() -> None:
    """
    Test that initializing a Vacancy with a non-integer salary raises a ValueError.

    This test ensures that the Vacancy constructor raises a ValueError when
    the salary is provided as a string instead of an integer. The expected
    exception message is 'Invalid salary_min'.
    """
    with pytest.raises(ValueError, match="Invalid salary_min"):
        Vacancy(
            vacancy_id="123",
            name="Software Engineer",
            url="http://example.com",
            description="Job description",
            salary="50000",
        )


def test_vacancy_str_method_formats_correctly() -> None:
    """
    Test that the str method of a Vacancy object formats correctly.

    This test ensures that the str method of a Vacancy object formats the
    object's attributes correctly. The expected output is a string that
    contains the vacancy id, name, salary, URL, and description of the
    vacancy, formatted as required by the task.

    Parameters:
    vacancy (Vacancy): The Vacancy object to test.

    Returns:
    None
    """
    vacancy = Vacancy(
        vacancy_id="123",
        name="Software Engineer",
        url="http://example.com",
        description="This is a job description",
        salary=50000,
    )
    expected_output = (
        "Номер: 123. Название: Software Engineer. "
        "Зарплата: 50000. Ссылка на вакансию: http://example.com. "
        "Описание: This is a job description"
    )
    assert str(vacancy) == expected_output


def test_vacancy_str_method_replaces_unicode_character() -> None:
    vacancy = Vacancy(
        vacancy_id="123",
        name="Software Engineer",
        url="http://example.com",
        description="This is a job description with a special character \u2060",
        salary=50000,
    )
    expected_output = (
        "Номер: 123. Название: Software Engineer. "
        "Зарплата: 50000. Ссылка на вакансию: http://example.com. "
        "Описание: This is a job description with a special character "
    )
    assert str(vacancy) == expected_output


def test_vacancy_str_method_formats_correctly_with_empty_description():
    vacancy = Vacancy(
        vacancy_id="123", name="Software Engineer", url="http://example.com", description="", salary=50000
    )
    expected_output = (
        "Номер: 123. Название: Software Engineer. "
        "Зарплата: 50000. Ссылка на вакансию: http://example.com. "
        "Описание: "
    )
    assert str(vacancy) == expected_output


def test_vacancy_str_method_formats_correctly_with_long_url():
    long_url = "http://" + "a" * 200 + ".com"
    vacancy = Vacancy(
        vacancy_id="123", name="Software Engineer", url=long_url, description="This is a job description", salary=50000
    )
    expected_output = (
        f"Номер: 123. Название: Software Engineer. "
        f"Зарплата: 50000. Ссылка на вакансию: {long_url}. "
        f"Описание: This is a job description"
    )
    assert str(vacancy) == expected_output


def test_cast_to_object_list_handles_convertible_salary() -> None:
    """
    Test that cast_to_object_list handles a vacancy with a non-integer salary that can be converted to an integer.

    This test ensures that when a vacancy dictionary has a salary that is a float,
    it is correctly converted to an integer and processed.
    """
    hh_vacancies = [
        {
            "id": "123",
            "name": "Software Engineer",
            "alternate_url": "http://example.com/1",
            "snippet": {"requirement": "Requirement 1", "responsibility": "Responsibility 1"},
            "salary": {"from": 50000.0, "to": 70000.0},
        }
    ]

    vacancies = Vacancy.cast_to_object_list(hh_vacancies)

    assert len(vacancies) == 1
    assert vacancies[0].vacancy_id == "123"
    assert vacancies[0].name == "Software Engineer"
    assert vacancies[0].salary == 60000  # Average of 50000 and 70000, rounded to integer


def test_cast_to_object_list_handles_special_characters_in_description() -> None:
    """
    Test that cast_to_object_list handles a vacancy with a description containing special characters correctly.

    This test ensures that when a vacancy dictionary has a description with special characters,
    it is processed correctly and included in the resulting list of Vacancy objects.
    """
    hh_vacancies = [
        {
            "id": "123",
            "name": "Software Engineer",
            "alternate_url": "http://example.com/1",
            "snippet": {"requirement": "Requirement with special character \u2060"},
            "salary": {"from": 50000, "to": 70000},
        }
    ]

    vacancies = Vacancy.cast_to_object_list(hh_vacancies)

    assert len(vacancies) == 1
    assert vacancies[0].vacancy_id == "123"
    assert vacancies[0].name == "Software Engineer"
    assert vacancies[0].description == "Requirement with special character "
    assert vacancies[0].salary == 60000  # Average of 50000 and 70000, rounded to integer


def test_cast_to_object_list_handles_long_name() -> None:
    """
    Test that cast_to_object_list handles a vacancy with a very long name without errors.

    This test ensures that when a vacancy dictionary has a very long name,
    it is processed correctly and included in the resulting list of Vacancy objects.
    """
    long_name = "Software Engineer" * 50  # Create a very long name by repeating a string
    hh_vacancies = [
        {
            "id": "123",
            "name": long_name,
            "alternate_url": "http://example.com/1",
            "snippet": {"requirement": "Requirement 1", "responsibility": "Responsibility 1"},
            "salary": {"from": 50000, "to": 70000},
        }
    ]

    vacancies = Vacancy.cast_to_object_list(hh_vacancies)

    assert len(vacancies) == 1
    assert vacancies[0].vacancy_id == "123"
    assert vacancies[0].name == long_name
    assert vacancies[0].salary == 60000  # Average of 50000 and 70000, rounded to integer


def test_cast_to_object_list_skips_vacancy_with_missing_name() -> None:
    """
    Test that cast_to_object_list skips a vacancy with a missing 'name' field and continues processing others.

    This test ensures that when a vacancy dictionary is missing the 'name' field,
    it is skipped, and the method continues processing other valid vacancies.
    """
    hh_vacancies = [
        {
            "id": "123",
            "name": "ETL Engineer",
            "alternate_url": "http://example.com/1",
            "snippet": {"requirement": "Requirement 1", "responsibility": "Responsibility 1"},
            "salary": {"from": 50000, "to": 70000},
        },
        {
            "id": "124",
            # Missing 'name' field
            "alternate_url": "http://example.com/2",
            "snippet": {"requirement": "Requirement 2", "responsibility": "Responsibility 2"},
            "salary": {"from": 60000, "to": 80000},
        },
        {
            "id": "125",
            "name": "Software Engineer",
            "alternate_url": "http://example.com/3",
            "snippet": {"requirement": "Requirement 3", "responsibility": "Responsibility 3"},
            "salary": {"from": 55000, "to": 75000},
        },
    ]

    vacancies = Vacancy.cast_to_object_list(hh_vacancies)

    assert len(vacancies) == 2
    assert vacancies[0].vacancy_id == "123"
    assert vacancies[0].name == "ETL Engineer"
    assert vacancies[1].vacancy_id == "125"
    assert vacancies[1].name == "Software Engineer"
