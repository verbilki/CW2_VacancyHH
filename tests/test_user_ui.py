from unittest.mock import patch

import pytest

from src.user_ui import get_query_params, get_top_vacancies, initial_load, print_vacancies
from src.vacancy import Vacancy


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


def test_get_top_vacancies_filters_by_salary(capsys: pytest.CaptureFixture):
    """
    Test that get_top_vacancies correctly filters out vacancies with salaries below the specified lower limit.

    This test uses patch to simulate user inputs for keywords, lower limit salary, and top N vacancies.
    It asserts that the function correctly filters vacancies based on the lower limit salary and prints
    only those that meet the criteria.
    """

    class Vacancy:
        def __init__(self, name, description, salary):
            self.name = name
            self.description = description
            self.salary = salary

        def __str__(self):
            return f"{self.name} with salary {self.salary}"

    # Create a list of vacancies with varying salaries
    vacancies = [
        Vacancy(name="Developer A", description="Python Developer", salary=50000),
        Vacancy(name="Developer B", description="Java Developer", salary=80000),
        Vacancy(name="Developer C", description="C++ Developer", salary=30000),
        Vacancy(name="Developer D", description="JavaScript Developer", salary=90000),
    ]

    # Simulate user input for filtering by salary
    with patch("builtins.input", side_effect=["", "60000", ""]):
        get_top_vacancies(vacancies)

    captured = capsys.readouterr()
    expected_output = (
        "Top-2 вакансий (отсортированных по убыванию зарплат):\n"
        "1. Developer D with salary 90000\n"
        "2. Developer B with salary 80000\n"
    )
    assert captured.out == expected_output, "Expected vacancies with salary above 60000 to be printed correctly"


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

    # Create a list of vacancies
    vacancies = [
        Vacancy(name="Developer A", description="Python Developer", salary=50000),
        Vacancy(name="Developer B", description="Java Developer", salary=80000),
        Vacancy(name="Developer C", description="C++ Developer", salary=30000),
        Vacancy(name="Developer D", description="JavaScript Developer", salary=90000),
    ]

    # Simulate user input for no keywords and zero salary limit
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

    # Create a list of vacancies with varying names and descriptions
    vacancies = [
        Vacancy(name="Python Developer", description="Experienced in Django", salary=70000),
        Vacancy(name="Java Developer", description="Spring Boot expert", salary=80000),
        Vacancy(name="C++ Engineer", description="Embedded systems", salary=75000),
        Vacancy(name="Full Stack Developer", description="React and Node.js", salary=85000),
    ]

    # Simulate user input for multiple keywords
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
