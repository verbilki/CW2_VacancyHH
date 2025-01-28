import os
from typing import List
from unittest import mock

from dotenv import load_dotenv

from src.file_json import JSONFunc
from src.vacancy import Vacancy


def test_get_data_returns_empty_list_when_file_contains_invalid_json():
    """
    Test that get_data method returns an empty list when the JSON file contains invalid JSON.

    This test ensures that the get_data method can handle invalid JSON in the file
    without raising an exception, and returns an empty list instead.
    """
    mock_open = mock.mock_open(read_data="{invalid_json: true")

    with mock.patch("builtins.open", mock_open):
        json_func = JSONFunc("")
        result = json_func.get_data()
        assert result == []
    mock_open = mock.mock_open(read_data="{invalid_json: true")

    with mock.patch("builtins.open", mock_open):
        json_func = JSONFunc("")
        result = json_func.get_data()
        assert result == []


def test_get_data_returns_empty_list_when_file_does_not_exist() -> None:
    """
    Test that get_data method returns an empty list when the JSON file does not exist.

    This test mocks the os.path.exists method to simulate the scenario where the file
    does not exist, ensuring that the get_data method correctly returns an empty list.
    """
    json_func = JSONFunc("non_existent_file.json")

    with mock.patch("os.path.exists", return_value=False):
        # Call the method
        result: List = json_func.get_data()

        # Assert that the result is an empty list
        assert result == []


def test_get_data_returns_list_when_file_contains_valid_json():
    """
    Test that get_data method returns a list of dictionaries when the JSON file contains valid JSON.

    This test ensures that the get_data method can handle valid JSON in the file
    and returns a list of dictionaries, where each dictionary represents a vacancy.
    """
    # Sample valid JSON data
    valid_json_data = (
        "["
        "{"
        '"id": "1", "name": "Vacancy 1", '
        '"url": "http://example.com/1", "description": "Description 1", "salary": "1000"'
        "},"
        "{"
        '"id": "2", "name": "Vacancy 2", '
        '"url": "http://example.com/2", "description": "Description 2", "salary": "2000"'
        "}"
        "]"
    )

    # Create a mock for the open function to simulate valid JSON content
    mock_open = mock.mock_open(read_data=valid_json_data)

    # Patch the open function in the JSONFunc module
    with mock.patch("builtins.open", mock_open), mock.patch("os.path.exists", return_value=True):
        load_dotenv()
        json_func = JSONFunc(os.path.join(os.getenv("FILEPATH", ""), ".json"))

        # Call the method
        result = json_func.get_data()

        # Assert that the result matches the expected list of vacancies
        expected_result = [
            {
                "id": "1",
                "name": "Vacancy 1",
                "url": "http://example.com/1",
                "description": "Description 1",
                "salary": "1000",
            },
            {
                "id": "2",
                "name": "Vacancy 2",
                "url": "http://example.com/2",
                "description": "Description 2",
                "salary": "2000",
            },
        ]
        assert result == expected_result


def test_add_vacancies(vacancies_fixture_1: list[Vacancy]):
    """
    Test that add_vacancies method adds the given vacancies to the JSON file.

    This test ensures that the add_vacancies method correctly adds the given
    vacancies to the JSON file, and that the get_data method returns the correct
    list of vacancies.
    """
    filepath = "test.json"
    with open(filepath, "w"):
        saver = JSONFunc(filepath)
        saver.add_vacancies(vacancies_fixture_1)
        data = saver.get_data()
        assert len(data) == 4
        assert data[0]["name"] == "Software Engineer"
        assert data[1]["name"] == "Data Scientist"
    filepath = "test.json"
    with open(filepath, "w"):
        saver = JSONFunc(filepath)
        saver.add_vacancies(vacancies_fixture_1)
        data = saver.get_data()
        assert len(data) == 4
        assert data[0]["name"] == "Software Engineer"
        assert data[1]["name"] == "Data Scientist"


def test_delete_vacancy(vacancies_fixture_1: list[Vacancy]):
    """
    Test that delete_vacancy method deletes the given vacancy from the JSON file.

    This test ensures that the delete_vacancy method correctly deletes the given
    vacancy from the JSON file, and that the get_data method returns the correct
    list of vacancies.
    """
    saver = JSONFunc("test.json")
    saver.add_vacancies(vacancies_fixture_1)
    saver.delete_vacancy("100")
    assert len(saver.get_data()) == 3
