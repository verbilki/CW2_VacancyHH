from typing import List
from unittest import mock

from src.file_json import JSONFunc


def test_get_data_returns_empty_list_when_file_contains_invalid_json():
    # Create a mock for the open function to simulate invalid JSON content
    mock_open = mock.mock_open(read_data="{invalid_json: true")

    # Patch the open function in the JSONFunc module
    with mock.patch("builtins.open", mock_open):
        json_func = JSONFunc()

        # Call the method
        result = json_func.get_data()

        # Assert that the result is an empty list
        assert result == []


def test_get_data_returns_empty_list_when_file_does_not_exist() -> None:
    """
    Test that get_data method returns an empty list when the JSON file does not exist.

    This test mocks the os.path.exists method to simulate the scenario where the file
    does not exist, ensuring that the get_data method correctly returns an empty list.
    """
    json_func = JSONFunc()

    with mock.patch("os.path.exists", return_value=False):
        # Call the method
        result: List = json_func.get_data()

        # Assert that the result is an empty list
        assert result == []


def test_get_data_returns_list_when_file_contains_valid_json():
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
        json_func = JSONFunc()

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
