import pytest

from src.vacancy import Vacancy

# def test_vacancy_init_raises_exception_on_long_description():
#     long_description = "a" * 1001
#     with pytest.raises(ValueError, match="Недопустимое описание вакансии"):
#         Vacancy(vacancy_id="123", name="Software Engineer", url="http://example.com", description=long_description,
#                 salary=50000)


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
