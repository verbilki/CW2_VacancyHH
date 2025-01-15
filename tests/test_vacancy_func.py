import pytest

from src.vacancy_func import (filter_vacancies, get_top_vacancies, get_vacancies_by_salary, print_vacancies,
                              sort_vacancies)


def test_filter_vacancies_no_match(vacancies_fixture_1: list):
    """
    Test that the filter_vacancies function returns an empty list when no descriptions contain the filter word.

    This test ensures that the filter_vacancies function can handle a filter word that does not appear in any of the
    descriptions. The test will pass if the function returns an empty list.

    Parameters:
    vacancies_fixture_1 (list): A list of Vacancy objects to be tested.

    Returns: None
    """
    filter_word = "Ruby"
    result = filter_vacancies(vacancies_fixture_1, filter_word)
    assert result == [], "Expected an empty list when no descriptions contain the filter word"


def test_filter_vacancies_empty_string(vacancies_fixture_1: list):
    """
    Test that the filter_vacancies function returns all vacancies when the filter word is an empty string.

    This test ensures that the filter_vacancies function can handle an empty string as its filter word,
    and will return all the vacancies in the list when given one.

    Parameters:
    vacancies_fixture_1 (list): A list of Vacancy objects to be tested.

    Returns: None
    """
    filter_word = ""
    result = filter_vacancies(vacancies_fixture_1, filter_word)
    assert result == vacancies_fixture_1, "Expected all vacancies to be returned when filter word is an empty string"


def test_filter_vacancies_with_substring_match(vacancies_fixture_1: list):
    """
    Test that the filter_vacancies function correctly handles filter words that are substrings of the descriptions.

    This test ensures that the filter_vacancies function can identify and return vacancies even when
    the filter word is a substring of the description. The function should match the filter word based
    on the content, ignoring any surrounding text.

    Parameters:
    vacancies_fixture_1 (list): A list of Vacancy objects to be tested.

    Returns: None
    """
    filter_word = "Developer"
    result = filter_vacancies(vacancies_fixture_1, filter_word)

    def test_get_top_vacancies_top_n_greater_than_vacancies():
        """
        Test that the get_top_vacancies function returns all vacancies
        when top_n is greater than the number of vacancies.

        This test ensures that the get_top_vacancies function can handle a case
        where the requested number of top vacancies exceeds the total number of available vacancies,
        and returns all available vacancies.

        Returns: None
        """

        class Vacancy:
            def __init__(self, description, salary):
                self.description = description
                self.salary = salary

        vacancies = [
            Vacancy(description="Developer A", salary=70000),
            Vacancy(description="Developer B", salary=50000),
            Vacancy(description="Developer C", salary=60000),
        ]
        top_n = 5  # Greater than the number of vacancies
        result = get_top_vacancies(vacancies, top_n)
        assert (
            result == vacancies
        ), "Expected all vacancies to be returned when top_n is greater than the number of vacancies"


# def test_get_top_vacancies_with_none_values():
#     """
#     Test that the get_top_vacancies function correctly handles a list of vacancies with None values
#     and returns the top_n non-None values.
#
#     This test ensures that the get_top_vacancies function can handle a list containing None values
#     and only considers non-None Vacancy objects when returning the top_n results.
#
#     Returns: None
#     """
#
#     class Vacancy:
#         def __init__(self, description, salary):
#             self.description = description
#             self.salary = salary
#
#     vacancies = [
#         Vacancy(description="Developer A", salary=70000),
#         None,
#         Vacancy(description="Developer B", salary=50000),
#         None,
#         Vacancy(description="Developer C", salary=60000),
#     ]
#     top_n = 2
#     # Filter out None values before passing to the function
#     filtered_vacancies = [vacancy for vacancy in vacancies if vacancy is not None]
#     result = get_top_vacancies(filtered_vacancies, top_n)
#     expected = [
#         filtered_vacancies[0],  # Developer A with salary 70000
#         filtered_vacancies[2],  # Developer C with salary 60000
#     ]
#     assert result == expected, "Expected the top 2 non-None vacancies to be returned"


def test_get_top_vacancies_with_duplicates():
    """
    Test that the get_top_vacancies function correctly handles a list of vacancies with duplicate entries
    and returns the top_n duplicates.

    This test ensures that the get_top_vacancies function can handle duplicate vacancies in the list
    and returns the correct number of top vacancies as specified by top_n.

    Returns: None
    """

    class Vacancy:
        def __init__(self, description, salary):
            self.description = description
            self.salary = salary

    vacancies = [
        Vacancy(description="Developer A", salary=70000),
        Vacancy(description="Developer A", salary=70000),
        Vacancy(description="Developer B", salary=50000),
        Vacancy(description="Developer B", salary=50000),
        Vacancy(description="Developer C", salary=60000),
        Vacancy(description="Developer C", salary=60000),
    ]
    top_n = 4
    result = get_top_vacancies(vacancies, top_n)
    expected = [
        vacancies[0],  # Developer A with salary 70000
        vacancies[1],  # Developer A with salary 70000
        vacancies[2],  # Developer B with salary 50000
        vacancies[3],  # Developer B with salary 50000
    ]
    assert result == expected, "Expected the top 4 vacancies to be returned, including duplicates"


def test_get_top_vacancies_negative_top_n():
    """
    Test that the get_top_vacancies function returns an empty list when top_n is negative.

    This test ensures that the get_top_vacancies function can handle a negative top_n value
    and returns an empty list, as it is not logical to request a negative number of top vacancies.

    Returns: None
    """

    class Vacancy:
        def __init__(self, description, salary):
            self.description = description
            self.salary = salary

    vacancies = [
        Vacancy(description="Developer A", salary=70000),
        Vacancy(description="Developer B", salary=50000),
        Vacancy(description="Developer C", salary=60000),
    ]
    top_n = -3  # Negative value
    result = get_top_vacancies(vacancies, top_n)
    assert result == [], "Expected an empty list when top_n is negative"


def test_get_top_vacancies_top_n_five():
    """
    Test that the get_top_vacancies function returns the first 5 vacancies when top_n is set to 5
    and there are more than 5 vacancies.

    This test ensures that the get_top_vacancies function correctly returns the specified number
    of top vacancies when the list contains more vacancies than requested.

    Returns: None
    """

    class Vacancy:
        def __init__(self, description, salary):
            self.description = description
            self.salary = salary

    vacancies = [
        Vacancy(description="Developer A", salary=70000),
        Vacancy(description="Developer B", salary=50000),
        Vacancy(description="Developer C", salary=60000),
        Vacancy(description="Developer D", salary=80000),
        Vacancy(description="Developer E", salary=75000),
        Vacancy(description="Developer F", salary=65000),
        Vacancy(description="Developer G", salary=72000),
    ]
    top_n = 5
    result = get_top_vacancies(vacancies, top_n)
    expected = vacancies[:5]  # First 5 vacancies
    assert result == expected, "Expected the first 5 vacancies to be returned when top_n is set to 5"


def test_filter_vacancies_with_special_characters(vacancies_fixture_2: list):
    """
    Test that the filter_vacancies function correctly handles filter words with special characters.

    This test ensures that the filter_vacancies function can identify and return vacancies even when
    the filter word contains special characters. The function should match the filter word based on
    the content, ignoring any special characters.

    Parameters:
    vacancies_fixture_2 (list): A list of Vacancy objects to be tested.

    Returns: None
    """
    filter_word = "C++"
    result = filter_vacancies(vacancies_fixture_2, filter_word)
    expected = [vacancies_fixture_2[0]]  # C++ Developer with experience in Qt framework
    assert result == expected, "Expected vacancies with descriptions containing 'C++' to be returned"


def test_filter_vacancies_does_not_modify_original_list(vacancies_fixture_1: list):
    """
    Test that the filter_vacancies function does not modify the original list of vacancies.

    This test ensures that calling the filter_vacancies function with a given filter word
    does not alter the original list of vacancies. The function is expected to return a new
    list containing the filtered results while leaving the input list unchanged.

    Parameters:
    vacancies_fixture_1 (list): A fixture providing a list of Vacancy objects to be tested.

    Returns: None
    """
    original_vacancies = vacancies_fixture_1[:]
    filter_word = "Developer"
    _ = filter_vacancies(vacancies_fixture_1, filter_word)
    assert vacancies_fixture_1 == original_vacancies, "Expected the original list of vacancies to remain unchanged"


def test_filter_vacancies_with_long_filter_word():
    """
    Test that the filter_vacancies function can handle long filter words.

    This test ensures that calling the filter_vacancies function with a long
    filter word (i.e., a filter word that is longer than a single word) will
    return the expected results. The test will pass if the function returns a
    list containing the expected Vacancy objects.

    Parameters:
    vacancies (list): A list of Vacancy objects to be tested.
    filter_word (str): A long filter word to be used for testing.

    Returns: None
    """

    class Vacancy:
        def __init__(self, description):
            self.description = description

    vacancies = [
        Vacancy(description="Senior Software Engineer with extensive experience in distributed systems"),
        Vacancy(description="Data Scientist with expertise in deep learning and neural networks"),
        Vacancy(description="Frontend Developer with a passion for creating intuitive user interfaces"),
    ]
    filter_word = "extensive experience in distributed systems"
    result = filter_vacancies(vacancies, filter_word)
    expected = [vacancies[0]]  # Senior Software Engineer with extensive experience in distributed systems
    assert result == expected, "Expected vacancies with descriptions containing the long filter word to be returned"


def test_filter_vacancies_with_leading_trailing_spaces() -> None:
    """
    Test that the filter_vacancies function correctly handles leading and trailing spaces in descriptions.

    This test ensures that the filter_vacancies function can identify and return vacancies even when
    the descriptions have leading or trailing spaces. The function should match the filter word based
    on the content, ignoring any surrounding whitespace.

    Returns: None
    """

    class Vacancy:
        def __init__(self, description):
            self.description = description

    vacancies = [
        Vacancy(description="  Software Engineer with Python experience  "),
        Vacancy(description="Data Scientist with machine learning skills"),
        Vacancy(description="  Frontend Developer with React knowledge"),
        Vacancy(description="Java Developer with Spring framework  "),
    ]
    filter_word = "Software Engineer"
    result = filter_vacancies(vacancies, filter_word)
    expected = [vacancies[0]]  # Software Engineer with Python experience
    assert result == expected, "Expected vacancies with descriptions containing 'Software Engineer' to be returned"


def test_get_vacancies_by_salary_all_below_threshold():
    """
    Test that the get_vacancies_by_salary function returns an empty list
    when all vacancies have salaries below the threshold.

    This test ensures that the get_vacancies_by_salary function correctly identifies when no vacancies
    meet the salary threshold and returns an empty list in such cases.

    Returns: None
    """

    class Vacancy:
        def __init__(self, description, salary):
            self.description = description
            self.salary = salary

    vacancies = [
        Vacancy(description="Junior Developer", salary=30000),
        Vacancy(description="Intern", salary=15000),
        Vacancy(description="Support Engineer", salary=25000),
    ]
    salary_threshold = 35000
    result = get_vacancies_by_salary(vacancies, salary_threshold)
    assert result == [], "Expected an empty list when all vacancies have salaries below the threshold"


def test_get_vacancies_by_salary_large_number_of_vacancies() -> None:
    """
    Test that the get_vacancies_by_salary function handles a large number of vacancies efficiently.

    This test ensures that the get_vacancies_by_salary function can process a large list of vacancies
    and correctly filter them based on the salary threshold without performance degradation.

    Returns: None
    """

    class Vacancy:
        def __init__(self, description, salary):
            self.description = description
            self.salary = salary

    # Create a large list of vacancies with varying salaries
    vacancies = [Vacancy(description=f"Vacancy {i}", salary=i * 1000) for i in range(1, 10001)]
    salary_threshold = 5000000
    result = get_vacancies_by_salary(vacancies, salary_threshold)

    # Expect vacancies with salaries greater than 5,000,000
    expected = [vacancy for vacancy in vacancies if vacancy.salary > salary_threshold]
    assert result == expected, "Expected vacancies with salaries greater than the threshold to be returned"


def test_get_vacancies_by_salary_extremely_high_threshold():
    """
    Test that the get_vacancies_by_salary function returns an empty list when the salary threshold is extremely high.

    This test ensures that the get_vacancies_by_salary function correctly identifies when no vacancies
    meet the salary threshold and returns an empty list in such cases.

    Returns: None
    """

    class Vacancy:
        def __init__(self, description, salary):
            self.description = description
            self.salary = salary

    vacancies = [
        Vacancy(description="Senior Developer", salary=120000),
        Vacancy(description="Project Manager", salary=110000),
        Vacancy(description="Data Analyst", salary=95000),
    ]
    salary_threshold = 200000
    result = get_vacancies_by_salary(vacancies, salary_threshold)
    assert result == [], "Expected an empty list when the salary threshold is extremely high"


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
        "Développeur Python with salary 70000\n"
        "Ingeniero de Software with salary 80000\n"
        "Разработчик на Java with salary 75000\n"
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
        "Developer A with salary 70000\n"
        "Developer A with salary 70000\n"
        "Developer B with salary 50000\n"
        "Developer B with salary 50000\n"
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
        "12345 with salary 70000\n"
        "['Developer', 'B'] with salary 50000\n"
        "{'role': 'Developer C'} with salary 60000\n"
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
    expected_output = f"{multiline_description} with salary 70000\n"
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
        "Developer A with C++ & Python with salary 70000\n"
        "Data Scientist (R&D) with salary 90000\n"
        "Frontend Developer - React.js with salary 80000\n"
    )
    assert (
        captured.out == expected_output
    ), "Expected each Vacancy object with special characters to be printed correctly"


def test_print_vacancies(capsys):
    """
    Test
    that
    the
    print_vacancies
    function
    prints
    each
    Vacancy
    object
    when
    given
    a
    list
    of
    Vacancy
    objects.

    This
    test
    ensures
    that
    the
    print_vacancies
    function
    correctly
    iterates
    over
    the
    list
    of
    Vacancy
    objects
    and prints
    each
    one
    to
    the
    standard
    output.

    Returns: None
    """

    class Vacancy:
        def __init__(self, description, salary):
            self.description = description
            self.salary = salary

        def __str__(self):
            return f"{self.description} with salary {self.salary}"

    vacancies = [
        Vacancy(description="Developer A", salary=70000),
        Vacancy(description="Developer B", salary=50000),
        Vacancy(description="Developer C", salary=60000),
    ]

    print_vacancies(vacancies)

    captured = capsys.readouterr()
    expected_output = (
        "Developer A with salary 70000\n" "Developer B with salary 50000\n" "Developer C with salary 60000\n"
    )
    assert captured.out == expected_output, "Expected each Vacancy object to be printed"
    vacancies = []
    result = sort_vacancies(vacancies)
    assert result == [], "Expected an empty list when sorting an empty list of vacancies"


def test_sort_vacancies_same_salary():
    """
    Test that the sort_vacancies function returns the same list when all vacancies have the same salary.

    This test ensures that the sort_vacancies function does not alter the order of vacancies
    when all salaries are identical, as there is no basis for sorting.

    Returns: None
    """

    class Vacancy:
        def __init__(self, description, salary):
            self.description = description
            self.salary = salary

    vacancies = [
        Vacancy(description="Developer A", salary=50000),
        Vacancy(description="Developer B", salary=50000),
        Vacancy(description="Developer C", salary=50000),
    ]
    result = sort_vacancies(vacancies)
    assert result == vacancies, "Expected the same list when all vacancies have the same salary"


def test_sort_vacancies_mixed_order_salaries():
    """
    Test that the sort_vacancies function correctly sorts vacancies when they have mixed order salaries.

    This test ensures that the sort_vacancies function can handle a list of vacancies with salaries
    in a mixed order and returns them sorted in ascending order by salary.

    Returns: None
    """

    class Vacancy:
        def __init__(self, description, salary):
            self.description = description
            self.salary = salary

    vacancies = [
        Vacancy(description="Developer A", salary=70000),
        Vacancy(description="Developer B", salary=50000),
        Vacancy(description="Developer C", salary=60000),
    ]
    result = sort_vacancies(vacancies)
    expected = [
        vacancies[1],  # Developer B with salary 50000
        vacancies[2],  # Developer C with salary 60000
        vacancies[0],  # Developer A with salary 70000
    ]
    assert result == expected, "Expected vacancies to be sorted in ascending order by salary"


def test_sort_vacancies_large_salaries():
    """
    Test that the sort_vacancies function correctly sorts vacancies when they have very large salary values.

    This test ensures that the sort_vacancies function can handle a list of vacancies with very large
    salary values and returns them sorted in ascending order by salary.

    Returns: None
    """

    class Vacancy:
        def __init__(self, description, salary):
            self.description = description
            self.salary = salary

    vacancies = [
        Vacancy(description="Developer A", salary=1000000000),
        Vacancy(description="Developer B", salary=500000000),
        Vacancy(description="Developer C", salary=1500000000),
    ]
    result = sort_vacancies(vacancies)
    expected = [
        vacancies[1],  # Developer B with salary 500000000
        vacancies[0],  # Developer A with salary 1000000000
        vacancies[2],  # Developer C with salary 1500000000
    ]
    assert result == expected, "Expected vacancies to be sorted in ascending order by large salary values"
