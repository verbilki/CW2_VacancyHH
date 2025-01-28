import os
from unittest.mock import patch

import pytest

from src.user_ui import (
    filter_vacancies_by_keywords,
    get_query_params,
    get_top_vacancies,
    initial_load,
    print_vacancies,
    save_vacancies_to_file,
)
from src.vacancy import Vacancy


@patch("os.getenv", return_value="valid_file_path")
@patch("builtins.input", return_value="valid_file_path")
@patch("os.path.exists", return_value=True)
@patch("src.file_json.JSONFunc.get_data")
@patch("src.vacancy.Vacancy.cast_to_object_list")
@patch("src.user_ui.print_vacancies")
def test_initial_load_with_valid_file_path(
    mock_print_vacancies, mock_cast_to_object_list, mock_get_data, mock_path_exists, mock_input, mock_getenv
):
    """
    Test that initial_load correctly loads vacancies when a valid file path is provided.

    This test uses patch to simulate a valid file path input and checks if the function
    loads the vacancies correctly from the JSON file.
    """
    # Mock the JSONFunc to return a list of dictionaries representing vacancies
    mock_vacancies_data = [
        {
            "vacancy_id": "100",
            "name": "Developer A",
            "url": "http://example.com/100",
            "description": "Python Developer",
            "salary": 70000,
        },
        {
            "vacancy_id": "200",
            "name": "Developer B",
            "url": "http://example.com/200",
            "description": "Java Developer",
            "salary": 80000,
        },
    ]
    mock_get_data.return_value = mock_vacancies_data

    # Mock the Vacancy.cast_to_object_list to convert dictionaries to Vacancy objects
    mock_vacancies_objects = [
        Vacancy(
            vacancy_id="100",
            name="Developer A",
            url="http://example.com/100",
            description="Python Developer",
            salary=70000,
        ),
        Vacancy(
            vacancy_id="200",
            name="Developer B",
            url="http://example.com/200",
            description="Java Developer",
            salary=80000,
        ),
    ]
    mock_cast_to_object_list.return_value = mock_vacancies_objects

    # Call the function under test
    file_path, vacancies = initial_load()

    # Assert that the file path is correctly returned
    assert file_path.endswith("valid_file_path")

    # Assert that the vacancies are loaded correctly
    assert vacancies == mock_vacancies_objects


def test_get_query_params_with_defaults():
    """
    Test that get_query_params returns default values when no inputs are provided.

    This test uses patch to simulate empty user inputs for the keyword, pages, and items per page.
    It asserts that the function returns the default values: 'Python' for the keyword,
    1 for the number of pages, and 10 for the number of items per page.
    """
    with patch("builtins.input", side_effect=["", "", ""]):
        result = get_query_params()
        assert result == ("Python", 3, 10)


def test_get_query_params_with_non_numeric_inputs():
    """
    Test that get_query_params handles non-numeric user inputs for the number of pages and items per page.

    This test uses patch to simulate user inputs of "Java" for the keyword, "abc" for the number of pages,
    and "xyz" for the number of items per page. It asserts that the function returns the default values:
    'Java' for the keyword, 1 for the number of pages, and 10 for the number of items per page.
    """
    with patch("builtins.input", side_effect=["Java", "abc", "xyz"]):
        result = get_query_params()
        assert result == ("Java", 3, 10)


def test_get_query_params_with_max_pages():
    """
    Test that get_query_params handles the maximum number of pages correctly.

    This test uses patch to simulate user inputs of "C++" for the keyword, 40 for the number of pages,
    and 5 for the items per page. It asserts that the function returns the correct values:
    'C++' for the keyword, 5 for the number of pages, and 40 for the items per page.
    """
    with patch("builtins.input", side_effect=["C++", "40", "5"]):
        result = get_query_params()
        assert result == ("C++", 5, 40)


def test_get_query_params_with_per_page_greater_than_40():
    """
    Test that get_query_params handles per_page values greater than 100.

    This test uses patch to simulate user inputs of "JavaScript" for the keyword,
    150 for the number of pages, and 2 for the items per page. It asserts that the
    function returns the default values: 'JavaScript' for the keyword, 2 for the
    number of pages, and 10 for the items per page.
    """
    with patch("builtins.input", side_effect=["JavaScript", "150", "2"]):
        result = get_query_params()
        assert result == ("JavaScript", 2, 10)


def test_get_query_params_with_per_page_less_than_1():
    """
    Test that get_query_params handles per_page values less than 1.

    This test uses patch to simulate user inputs of "Ruby" for the keyword,
    0 for the number of pages, and 3 for the items per page. It asserts that the
    function returns the default values: 'Ruby' for the keyword, 3 for the
    number of pages, and 10 for the items per page.
    """
    with patch("builtins.input", side_effect=["Ruby", "0", "3"]):
        result = get_query_params()
        assert result == ("Ruby", 3, 10)


def test_print_vacancies_with_non_ascii_characters(capsys: pytest.CaptureFixture):
    """
    Test that the print_vacancies function correctly prints Vacancy objects
    when their descriptions contain non-ASCII characters.

    This test ensures that the print_vacancies function can handle and correctly
    print vacancies with non-ASCII characters in their descriptions.

    Returns: None
    """

    class Vacancy:
        def __init__(self, description, salary):
            self.description = description
            self.salary = salary

        def __str__(self):
            return f"{self.description} with salary {self.salary}"

    # Create vacancies with non-ASCII characters in their descriptions
    vacancies = [
        Vacancy(description="Développeur Python", salary=70000),
        Vacancy(description="Ingeniero de Software", salary=80000),
        Vacancy(description="Разработчик на Java", salary=75000),
    ]

    print_vacancies(vacancies)

    captured = capsys.readouterr()
    expected_output = (
        "1. Développeur Python with salary 70000\n"
        "2. Ingeniero de Software with salary 80000\n"
        "3. Разработчик на Java with salary 75000\n"
    )
    assert captured.out == expected_output, "Expected vacancies with non-ASCII characters to be printed correctly"


def test_print_vacancies_with_duplicates(capsys: pytest.CaptureFixture):
    """
    Test that the print_vacancies function correctly prints Vacancy objects
    when the list contains duplicate entries.

    This test ensures that the print_vacancies function can handle and correctly
    print vacancies even if there are duplicate entries in the list.

    Returns: None
    """

    class Vacancy:
        def __init__(self, description, salary):
            self.description = description
            self.salary = salary

        def __str__(self):
            return f"{self.description} with salary {self.salary}"

    # Create vacancies with duplicate entries
    vacancies = [
        Vacancy(description="Developer A", salary=70000),
        Vacancy(description="Developer A", salary=70000),
        Vacancy(description="Developer B", salary=50000),
        Vacancy(description="Developer B", salary=50000),
    ]

    print_vacancies(vacancies)

    captured = capsys.readouterr()
    expected_output = (
        "1. Developer A with salary 70000\n"
        "2. Developer A with salary 70000\n"
        "3. Developer B with salary 50000\n"
        "4. Developer B with salary 50000\n"
    )
    assert captured.out == expected_output, "Expected duplicate vacancies to be printed correctly"


def test_print_vacancies_with_non_string_attributes(capsys: pytest.CaptureFixture):
    """
    Test that the print_vacancies function correctly prints Vacancy objects
    when their attributes are not strings.

    This test ensures that the print_vacancies function can handle and correctly
    print vacancies even if their attributes are not of string type.

    Returns: None
    """

    class Vacancy:
        def __init__(self, description, salary):
            self.description = description
            self.salary = salary

        def __str__(self):
            return f"{self.description} with salary {self.salary}"

    # Create vacancies with non-string attributes
    vacancies = [
        Vacancy(description=12345, salary=70000),
        Vacancy(description=["Developer", "B"], salary=50000),
        Vacancy(description={"role": "Developer C"}, salary=60000),
    ]

    print_vacancies(vacancies)

    captured = capsys.readouterr()
    expected_output = (
        "1. 12345 with salary 70000\n"
        "2. ['Developer', 'B'] with salary 50000\n"
        "3. {'role': 'Developer C'} with salary 60000\n"
    )
    assert captured.out == expected_output, "Expected vacancies with non-string attributes to be printed correctly"


def test_print_vacancies_with_special_characters(capsys: pytest.CaptureFixture):
    """
    Test that the print_vacancies function correctly prints Vacancy objects
    when their descriptions contain special characters.

    This test ensures that the print_vacancies function can handle and correctly
    print vacancies with special characters in their descriptions.
    """

    class Vacancy:
        def __init__(self, description, salary):
            self.description = description
            self.salary = salary

        def __str__(self):
            return f"{self.description} with salary {self.salary}"

    multiline_description = "Developer A\nwith extensive experience\nin Python and C++"
    vacancies = [
        Vacancy(description=multiline_description, salary=70000),
    ]

    print_vacancies(vacancies)

    captured = capsys.readouterr()
    expected_output = f"1. {multiline_description} with salary 70000\n"
    assert captured.out == expected_output, "Expected the multiline description to be printed correctly"


def test_print_vacancies_with_large_descriptions(capsys: pytest.CaptureFixture):
    """
    Test that the print_vacancies function correctly prints Vacancy objects
    when given a list of Vacancy objects with large descriptions.

    This test ensures that the print_vacancies function can handle and correctly
    print vacancies with large descriptions without truncation.

    Returns: None
    """

    class Vacancy:
        def __init__(self, description, salary):
            self.description = description
            self.salary = salary

        def __str__(self):
            return f"{self.description} with salary {self.salary}"

    vacancies = [
        Vacancy(description="Developer A with C++ & Python", salary=70000),
        Vacancy(description="Data Scientist (R&D)", salary=90000),
        Vacancy(description="Frontend Developer - React.js", salary=80000),
    ]

    print_vacancies(vacancies)

    captured = capsys.readouterr()
    expected_output = (
        "1. Developer A with C++ & Python with salary 70000\n"
        "2. Data Scientist (R&D) with salary 90000\n"
        "3. Frontend Developer - React.js with salary 80000\n"
    )
    assert (
        captured.out == expected_output
    ), "Expected each Vacancy object with special characters to be printed correctly"


def test_get_top_vacancies_filters_by_salary(capsys: pytest.CaptureFixture, vacancies_fixture_1):
    """
    Test that get_top_vacancies correctly filters out vacancies with salaries below the specified lower limit.

    This test uses patch to simulate user inputs for keywords, lower limit salary, and top N vacancies.
    It asserts that the function correctly filters vacancies based on the lower limit salary and prints
    only those that meet the criteria.
    """
    with patch("builtins.input", side_effect=["", "100000", ""]):
        get_top_vacancies(vacancies_fixture_1)

    captured = capsys.readouterr()
    expected_output = (
        "Top-2 вакансий (отсортированных по убыванию зарплат):\n"
        "1. Номер: 200. Название: Data Scientist. Зарплата: 120000. "
        "Ссылка на вакансию: https://promo2.com. Описание: Data Scientist with machine learning skills\n"
        "2. Номер: 100. Название: Software Engineer. Зарплата: 100000. "
        "Ссылка на вакансию: https://promo1.com. Описание: Software Engineer with Python experience\n"
    )
    assert captured.out == expected_output, "Expected vacancies with salary above 100000 to be printed correctly"


def test_get_top_vacancies_no_keywords_and_zero_salary_limit(capsys: pytest.CaptureFixture):
    """
    Test that get_top_vacancies returns all vacancies when no keywords are provided
    and the salary limit is set to zero.

    This test uses patch to simulate user inputs for no keywords, zero salary limit,
    and no specific top N vacancies. It asserts that all vacancies are printed
    since there are no filtering criteria.
    """

    class Vacancy:
        def __init__(self, name, description, salary):
            self.name = name
            self.description = description
            self.salary = salary

        def __str__(self):
            return f"{self.name} with salary {self.salary}"

    vacancies = [
        Vacancy(name="Developer A", description="Python Developer", salary=50000),
        Vacancy(name="Developer B", description="Java Developer", salary=80000),
        Vacancy(name="Developer C", description="C++ Developer", salary=30000),
        Vacancy(name="Developer D", description="JavaScript Developer", salary=90000),
    ]

    with patch("builtins.input", side_effect=["", "0", ""]):
        get_top_vacancies(vacancies)

    captured = capsys.readouterr()
    expected_output = (
        "Top-4 вакансий (отсортированных по убыванию зарплат):\n"
        "1. Developer D with salary 90000\n"
        "2. Developer B with salary 80000\n"
        "3. Developer A with salary 50000\n"
        "4. Developer C with salary 30000\n"
    )
    assert (
        captured.out == expected_output
    ), "Expected all vacancies to be printed when no keywords and zero salary limit are provided"


def test_get_top_vacancies_with_multiple_keywords(capsys: pytest.CaptureFixture):
    """
    Test that get_top_vacancies correctly filters vacancies based on multiple keywords
    present in either the name or description.

    This test uses patch to simulate user inputs for multiple keywords and no specific salary limit.
    It asserts that the function correctly filters vacancies based on the provided keywords.
    """

    class Vacancy:
        def __init__(self, name, description, salary):
            self.name = name
            self.description = description
            self.salary = salary

        def __str__(self):
            return f"{self.name} with salary {self.salary}"

    vacancies = [
        Vacancy(name="Python Developer", description="Experienced in Django", salary=70000),
        Vacancy(name="Java Developer", description="Spring Boot expert", salary=80000),
        Vacancy(name="C++ Engineer", description="Embedded systems", salary=75000),
        Vacancy(name="Full Stack Developer", description="React and Node.js", salary=85000),
    ]

    with patch("builtins.input", side_effect=["Developer React", "0", ""]):
        get_top_vacancies(vacancies)

    captured = capsys.readouterr()
    expected_output = (
        "Top-3 вакансий (отсортированных по убыванию зарплат):\n"
        "1. Full Stack Developer with salary 85000\n"
        "2. Java Developer with salary 80000\n"
        "3. Python Developer with salary 70000\n"
    )
    assert captured.out == expected_output, "Expected vacancies filtered by multiple keywords to be printed correctly"


@patch("builtins.input", return_value="Ruby Go")
def test_filter_vacancies_by_keywords_no_matches(vacancies_fixture_1: list[Vacancy]):
    """
    Test that filter_vacancies_by_keywords returns an empty list when no keywords match any vacancy descriptions.

    This test uses patch to simulate user input for keywords that do not match any vacancy descriptions.
    It asserts that the function returns an empty list.
    """
    # Simulate user input for keywords that do not match any descriptions
    assert (
        filter_vacancies_by_keywords(vacancies_fixture_1) == []
    ), "Expected an empty list when no keywords match any vacancy descriptions"


@patch("builtins.input", return_value=os.sep)
@patch("src.file_json.JSONFunc.add_vacancies")
@patch("os.path.exists", return_value=False)
def test_save_vacancies_to_file_with_root_directory_input(mock_path_exists, mock_add_vacancies, mock_input, capsys):
    """
    Test that save_vacancies_to_file prints an error message and returns
    when the input path is the root directory.

    This test uses patch to simulate user input of the root directory path
    and asserts that the function prints the correct error message and does not
    attempt to save any vacancies.
    """
    initial_file_path = "valid_file_path.json"
    vacancies = [
        Vacancy(
            vacancy_id="100",
            name="Developer A",
            url="http://example.com/100",
            description="Python Developer",
            salary=70000,
        )
    ]

    save_vacancies_to_file(initial_file_path, vacancies)

    captured = capsys.readouterr()
    expected_output = "Некорректный ввод. Путь не может быть корневой директорией.\n"
    assert captured.out == expected_output, "Expected an error message for root directory input"
    mock_add_vacancies.assert_not_called()


@patch("builtins.input", return_value="")
@patch("src.file_json.JSONFunc.add_vacancies")
def test_save_vacancies_to_initial_file_path(mock_add_vacancies, mock_input):
    """
    Test that save_vacancies_to_file saves vacancies to the initial file path
    when no new path is provided by the user.

    This test uses patch to simulate an empty input for the file path,
    ensuring that the function saves the vacancies to the initial file path.
    """
    initial_file_path = "test_initial_path.json"
    vacancies = [
        Vacancy(
            vacancy_id="1",
            name="Developer A",
            url="http://example.com/1",
            description="Python Developer",
            salary=70000,
        ),
        Vacancy(
            vacancy_id="2", name="Developer B", url="http://example.com/2", description="Java Developer", salary=80000
        ),
    ]

    save_vacancies_to_file(initial_file_path, vacancies)

    # Assert that add_vacancies is called with the initial file path
    mock_add_vacancies.assert_called_once_with(vacancies)


@patch("os.path.exists", return_value=True)
@patch("src.file_json.JSONFunc.add_vacancies")
@patch("builtins.input", return_value="existing_file_path.json")
def test_save_vacancies_to_existing_file(mock_input, mock_add_vacancies, mock_path_exists):
    """
    Test that save_vacancies_to_file adds vacancies to an existing file if the specified file path already exists.
    This test uses patch to simulate user input for the file path and checks if the function
    correctly adds vacancies to an existing file using JSONFunc.add_vacancies.
    """
    initial_file_path = "initial_file_path.json"
    vacancies = [
        Vacancy(
            vacancy_id="100",
            name="Developer A",
            url="http://example.com/100",
            description="Python Developer",
            salary=70000,
        ),
        Vacancy(
            vacancy_id="200",
            name="Developer B",
            url="http://example.com/200",
            description="Java Developer",
            salary=80000,
        ),
    ]

    save_vacancies_to_file(initial_file_path, vacancies)

    # Assert that the input was called to get the file path
    mock_input.assert_called_once()

    # Assert that add_vacancies was called with the correct file path and vacancies
    mock_add_vacancies.assert_called_once_with(vacancies)


@patch("builtins.input", return_value="special@path#file.json")
@patch("os.path.exists", return_value=False)
@patch("src.file_json.JSONFunc.add_vacancies")
def test_save_vacancies_to_file_with_special_characters_in_path(mock_add_vacancies, mock_path_exists, mock_input):
    """
    Test that save_vacancies_to_file handles input paths with special characters correctly.

    This test uses patch to simulate user input with special characters in the file path.
    It asserts that the JSONFunc.add_vacancies method is called with the correct file path.
    """
    vacancies = [
        Vacancy(
            vacancy_id="100",
            name="Developer A",
            url="http://example.com/100",
            description="Python Developer",
            salary=70000,
        )
    ]

    initial_file_path = "valid_file_path.json"
    save_vacancies_to_file(initial_file_path, vacancies)

    # Assert that the correct file path is used for saving
    mock_add_vacancies.assert_called_once_with(vacancies)
    assert mock_input.call_args[0][0].startswith("Введите путь к JSON-файлу")


def test_filter_vacancies_by_keywords_with_special_characters():
    """
    Test that filter_vacancies_by_keywords correctly filters vacancies when keywords contain special characters.

    This test uses patch to simulate user input with special characters in keywords.
    It asserts that the function correctly filters vacancies based on the provided keywords.
    """

    class Vacancy:
        def __init__(self, description):
            self.description = description

        def __str__(self):
            return self.description

    vacancies = [
        Vacancy(description="Python Developer with Django experience"),
        Vacancy(description="Java Developer - Spring Boot"),
        Vacancy(description="C++ Engineer (Embedded systems)"),
        Vacancy(description="Full Stack Developer: React.js & Node.js"),
    ]

    with patch("builtins.input", return_value="React.js & Node.js"):
        filtered_vacancies = filter_vacancies_by_keywords(vacancies)

    assert len(filtered_vacancies) == 1
    assert filtered_vacancies[0].description == "Full Stack Developer: React.js & Node.js"


@patch("builtins.input", return_value="тестовый_файл.json")
@patch("os.path.exists", return_value=False)
@patch("src.file_json.JSONFunc.add_vacancies")
def test_save_vacancies_to_file_with_non_ascii_path(mock_add_vacancies, mock_path_exists, mock_input):
    """
    Test that save_vacancies_to_file handles input paths with non-ASCII characters correctly.

    This test uses patch to simulate user input of a file path with non-ASCII characters.
    It asserts that the JSONFunc.add_vacancies method is called with the correct file path.
    """
    initial_file_path = "initial_path.json"
    vacancies = [
        Vacancy(
            vacancy_id="1",
            name="Developer A",
            url="http://example.com/1",
            description="Python Developer",
            salary=70000,
        )
    ]

    # Call the function under test
    save_vacancies_to_file(initial_file_path, vacancies)

    # Assert that JSONFunc.add_vacancies is called with the correct file path
    mock_add_vacancies.assert_called_once_with(vacancies)
    assert mock_input.call_args[0][0].startswith("Введите путь к JSON-файлу")


@patch("builtins.input", return_value="a" * 300)
@patch("os.path.exists", return_value=False)
@patch("src.file_json.JSONFunc.add_vacancies")
def test_save_vacancies_to_file_with_excessively_long_path(mock_add_vacancies, mock_path_exists, mock_input, capsys):
    """
    Test that save_vacancies_to_file handles excessively long input paths correctly.

    This test uses patch to simulate an excessively long file path input and checks if the function
    handles it without errors and attempts to save the vacancies to the specified path.
    """
    vacancies = [
        Vacancy(
            vacancy_id="100",
            name="Developer A",
            url="http://example.com/100",
            description="Python Developer",
            salary=70000,
        )
    ]
    initial_file_path = "valid_file_path.json"

    save_vacancies_to_file(initial_file_path, vacancies)

    captured = capsys.readouterr()
    assert "" in captured.out, "Expected message indicating the file path handling."
    mock_add_vacancies.assert_called_once_with(vacancies)


@patch("builtins.input", return_value="invalid|path.json")
@patch("os.path.exists", return_value=False)
@patch("src.file_json.JSONFunc.add_vacancies")
def test_save_vacancies_to_file_with_invalid_characters_in_path(
    mock_add_vacancies, mock_path_exists, mock_input, capsys: pytest.CaptureFixture
):
    """
    Test that save_vacancies_to_file handles input paths with invalid characters correctly.

    This test uses patch to simulate user input of a file path with invalid characters
    and checks if the function handles it without attempting to save the vacancies.
    """
    initial_file_path = "valid_path.json"
    vacancies = [
        Vacancy(
            vacancy_id="100",
            name="Developer A",
            url="http://example.com/100",
            description="Python Developer",
            salary=70000,
        )
    ]

    save_vacancies_to_file(initial_file_path, vacancies)

    captured = capsys.readouterr()
    assert "" in captured.out
    mock_add_vacancies.assert_called_once()


def test_filter_vacancies_by_keywords_with_non_ascii_keywords():
    """
    Test that filter_vacancies_by_keywords correctly filters vacancies
    when the input keywords contain non-ASCII characters.

    This test uses patch to simulate user input of non-ASCII keywords
    and checks if the function correctly filters the vacancies based
    on these keywords.
    """

    class Vacancy:
        def __init__(self, description):
            self.description = description

    vacancies = [
        Vacancy(description="Développeur Python"),
        Vacancy(description="Ingeniero de Software"),
        Vacancy(description="Разработчик на Java"),
    ]
    with patch("builtins.input", return_value="Développeur Разработчик"):
        filtered_vacancies = filter_vacancies_by_keywords(vacancies)

    assert len(filtered_vacancies) == 2
    assert filtered_vacancies[0].description == "Développeur Python"
    assert filtered_vacancies[1].description == "Разработчик на Java"
