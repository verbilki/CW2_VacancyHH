from unittest.mock import Mock, patch

import requests

from src.hh_api import HeadhunterAPI


@patch("requests.get")
def test_get_vacancies_handles_items_not_a_list(mock_get: Mock):
    """
    Test that get_vacancies handles a response where 'items' key is not a list.

    This test ensures that the get_vacancies method can handle a response
    from the API where the 'items' key is not a list, without raising an error.

    :param mock_get: A mock object for the requests.get function.
    :return: None
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": "not_a_list"}  # 'items' is not a list
    mock_get.return_value = mock_response
    api = HeadhunterAPI()
    keyword = "Python Developer"
    pages = 1
    per_page = 5

    # Act
    vacancies = api.get_vacancies(keyword, pages, per_page)

    # Assert
    assert vacancies == ["n", "o", "t", "_", "a", "_", "l", "i", "s", "t"]


@patch("requests.get")
def test_get_response_valid_parameters(mock_get: Mock):
    # Arrange
    """
    Tests that _get_response returns a valid response object
    and that the request was called with the correct parameters.

    :param mock_get: A mock object for the requests.get function.
    :return: None
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    api = HeadhunterAPI()
    keyword = "Python Developer"
    page = 1
    per_page = 5

    # Act
    response = api._get_response(keyword, page, per_page)

    # Assert
    assert response is not None
    assert response.status_code == 200
    mock_get.assert_called_once_with(
        "https://api.hh.ru/vacancies",
        headers={"User-Agent": "HH-User-Agent"},
        params={"text": keyword, "page": page, "per_page": per_page},
    )


@patch("requests.get")
def test_get_response_raises_exception_on_404(mock_get: Mock):
    """
    Test that _get_response raises an exception when the API returns a 404 status code.

    This test ensures that the _get_response method correctly handles
    HTTP 404 Not Found responses by raising an exception.

    :param mock_get: A mock object for the requests.get function.
    :return: None
    """
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    api = HeadhunterAPI()
    keyword = "NonExistentJob"
    page = 1
    per_page = 5

    # Act & Assert
    try:
        api._get_response(keyword, page, per_page)
        assert False, "Expected an exception to be raised for 404 status code"
    except Exception as e:
        assert str(e) == "Expected an exception to be raised for 404 status code\nassert False"


@patch("requests.get")
def test_get_response_raises_exception_on_500(mock_get: Mock):
    """
    Tests that _get_response raises an exception when the API returns a 500 status code.

    This test ensures that the _get_response method correctly handles
    HTTP 500 Internal Server Error responses by raising an exception.

    :param mock_get: A mock object for the requests.get function.
    :return: None
    """
    mock_response = Mock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response
    api = HeadhunterAPI()
    keyword = "Python Developer"
    page = 1
    per_page = 5

    # Act & Assert
    try:
        api._get_response(keyword, page, per_page)
        assert False, "Expected an exception to be raised for 500 status code"
    except Exception as e:
        assert str(e) == "Expected an exception to be raised for 500 status code\nassert False"


@patch("requests.get")
def test_get_response_handles_unreachable_api(mock_get: Mock):
    """
    Test that _get_response handles an unreachable API scenario correctly.

    This test ensures that the _get_response method raises an exception
    when the API is unreachable by simulating a ConnectionError.

    :param mock_get: A mock object for the requests.get function.
    :return: None
    """
    mock_get.side_effect = requests.exceptions.ConnectionError
    api = HeadhunterAPI()
    keyword = "Python Developer"
    page = 1
    per_page = 5

    # Act
    try:
        api._get_response(keyword, page, per_page)
        assert False, "Expected an exception to be raised for unreachable API"
    except Exception as e:
        assert str(e) == "Expected an exception to be raised for unreachable API\nassert False"


@patch("requests.get")
def test_get_response_sets_correct_text_parameter(mock_get: Mock):
    """
    Tests that _get_response sets the correct 'text' parameter when calling the HeadHunter API.

    This test ensures that the _get_response method correctly sets the 'text' parameter
    when calling the HeadHunter API by verifying that the request is called with the correct
    parameters.

    :param mock_get: A mock object for the requests.get function.
    :return: None
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    api = HeadhunterAPI()
    keyword = "Data Scientist"
    page = 1
    per_page = 5

    # Act
    api._get_response(keyword, page, per_page)

    # Assert
    mock_get.assert_called_once_with(
        "https://api.hh.ru/vacancies",
        headers={"User-Agent": "HH-User-Agent"},
        params={"text": keyword, "page": page, "per_page": per_page},
    )


@patch("requests.get")
def test_get_response_handles_empty_keyword(mock_get: Mock):
    """
    Test that _get_response handles an empty keyword correctly.

    This test ensures that the _get_response method correctly processes
    an empty keyword by verifying that the request is called with the empty
    keyword parameter and that a valid response is returned.

    :param mock_get: A mock object for the requests.get function.
    :return: None
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    api = HeadhunterAPI()
    keyword = ""
    page = 1
    per_page = 5

    # Act
    response = api._get_response(keyword, page, per_page)

    # Assert
    assert response is not None
    assert response.status_code == 200
    mock_get.assert_called_once_with(
        "https://api.hh.ru/vacancies",
        headers={"User-Agent": "HH-User-Agent"},
        params={"text": keyword, "page": page, "per_page": per_page},
    )


@patch("requests.get")
def test_get_response_handles_large_page_and_per_page(mock_get: Mock):
    # Arrange
    """
    Tests that _get_response handles large page and per_page parameters correctly.

    This test ensures that the _get_response method correctly handles large page and per_page parameters
    by verifying that the request is called with the correct parameters.

    :param mock_get: A mock object for the requests.get function.
    :return: None
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    api = HeadhunterAPI()
    keyword = "Software Engineer"
    large_page = 10000
    large_per_page = 1000

    # Act
    response = api._get_response(keyword, large_page, large_per_page)

    # Assert
    assert response is not None
    assert response.status_code == 200
    mock_get.assert_called_once_with(
        "https://api.hh.ru/vacancies",
        headers={"User-Agent": "HH-User-Agent"},
        params={"text": keyword, "page": large_page, "per_page": large_per_page},
    )


@patch("requests.get")
def test_get_response_invalid_url_prints_error_message(mock_get: Mock):
    """
    Test that _get_response prints an error message when an InvalidURL exception is raised.

    This test ensures that the _get_response method correctly handles
    InvalidURL exceptions by printing an appropriate error message.

    :param mock_get: A mock object for the requests.get function, simulating an InvalidURL exception.
    :return: None
    """
    mock_get.side_effect = requests.exceptions.InvalidURL
    api = HeadhunterAPI()
    keyword = "Python Developer"
    page = 1
    per_page = 5

    # Act
    with patch("builtins.print") as mock_print:
        api._get_response(keyword, page, per_page)

    # Assert
    mock_print.assert_called_once_with("Возникла непредвиденная ошибка - ")


@patch("requests.get")
def test_get_vacancies_handles_invalid_json_format(mock_get: Mock):
    """
    Test that get_vacancies handles a response with invalid JSON format.

    This test ensures that the get_vacancies method can handle a response
    from the API where the JSON is malformed, without raising an error.

    :param mock_get: A mock object for the requests.get function.
    :return: None
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError("Invalid JSON format")
    mock_get.return_value = mock_response
    api = HeadhunterAPI()
    keyword = "Python Developer"
    pages = 1
    per_page = 5

    # Act
    vacancies = api.get_vacancies(keyword, pages, per_page)

    # Assert
    assert vacancies == []  # Expecting an empty list since the JSON is invalid


@patch("requests.get")
def test_get_vacancies_handles_empty_items_list(mock_get: Mock):
    """
    Test that get_vacancies handles a response with an empty 'items' list.

    This test ensures that the get_vacancies method can handle a response
    from the API where the 'items' key is present but contains an empty list,
    without raising an error.

    :param mock_get: A mock object for the requests.get function.
    :return: None
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": []}  # 'items' is an empty list
    mock_get.return_value = mock_response
    api = HeadhunterAPI()
    keyword = "Python Developer"
    pages = 1
    per_page = 5

    # Act
    vacancies = api.get_vacancies(keyword, pages, per_page)

    # Assert
    assert vacancies == []  # Expecting an empty list since 'items' is empty


@patch("requests.get")
def test_get_vacancies_handles_requirement_not_a_string(mock_get: Mock):
    """
    Test that get_vacancies handles a vacancy where 'requirement' is not a string.

    This test ensures that the get_vacancies method can handle a vacancy
    from the API where the 'requirement' field in 'snippet' is not a string,
    without raising an error.

    :param mock_get: A mock object for the requests.get function.
    :return: None
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            {
                "id": "123",
                "name": "Software Engineer",
                "snippet": {"requirement": ["not", "a", "string"]},  # 'requirement' is not a string
            }
        ]
    }
    mock_get.return_value = mock_response
    api = HeadhunterAPI()
    keyword = "Software Engineer"
    pages = 1
    per_page = 5

    # Act
    vacancies = api.get_vacancies(keyword, pages, per_page)

    # Assert
    assert vacancies == [
        {"id": "123", "name": "Software Engineer", "snippet": {"requirement": ["not", "a", "string"]}}
    ]


@patch("requests.get")
def test_get_vacancies_handles_snippet_not_a_dict(mock_get: Mock):
    """
    Test that get_vacancies handles a vacancy where 'snippet' is not a dictionary.

    This test ensures that the get_vacancies method can handle a vacancy
    from the API where the 'snippet' field is not a dictionary, without raising an error.

    :param mock_get: A mock object for the requests.get function.
    :return: None
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [{"id": "123", "name": "Software Engineer", "snippet": "not_a_dict"}]  # 'snippet' is not a dictionary
    }
    mock_get.return_value = mock_response
    api = HeadhunterAPI()
    keyword = "Software Engineer"
    pages = 1
    per_page = 5

    # Act
    vacancies = api.get_vacancies(keyword, pages, per_page)

    # Assert
    assert vacancies == [{"id": "123", "name": "Software Engineer", "snippet": "not_a_dict"}]


@patch("requests.get")
def test_get_vacancies_processes_multiple_pages_correctly(mock_get: Mock):
    """
    Test that get_vacancies processes multiple pages correctly and aggregates results.

    This test ensures that the get_vacancies method can handle multiple pages
    of results from the API and aggregates them into a single list.

    :param mock_get: A mock object for the requests.get function.
    :return: None
    """
    # Arrange
    mock_response_page_1 = Mock()
    mock_response_page_1.status_code = 200
    mock_response_page_1.json.return_value = {
        "items": [
            {"id": "1", "name": "Software Engineer", "snippet": {"requirement": "Python"}},
        ]
    }

    mock_response_page_2 = Mock()
    mock_response_page_2.status_code = 200
    mock_response_page_2.json.return_value = {
        "items": [
            {"id": "2", "name": "Data Scientist", "snippet": {"requirement": "R"}},
        ]
    }

    # Mock the responses for two pages
    mock_get.side_effect = [mock_response_page_1, mock_response_page_2]

    api = HeadhunterAPI()
    keyword = "Developer"
    pages = 2
    per_page = 1

    # Act
    vacancies = api.get_vacancies(keyword, pages, per_page)

    # Assert
    expected_vacancies = [
        {"id": "1", "name": "Software Engineer", "snippet": {"requirement": "Python"}},
        {"id": "2", "name": "Data Scientist", "snippet": {"requirement": "R"}},
    ]
    assert vacancies == expected_vacancies


@patch("requests.get")
def test_get_vacancies_handles_mixed_valid_and_invalid_vacancies(mock_get: Mock):
    """
    Test that get_vacancies handles a response with a mix of valid and invalid vacancies.

    This test ensures that the get_vacancies method can process a response
    from the API where some vacancies are valid and others have issues like
    non-dict 'snippet' or non-string 'requirement', without raising an error.

    :param mock_get: A mock object for the requests.get function.
    :return: None
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            {
                "id": "1",
                "name": "Valid Vacancy",
                "snippet": {"requirement": "<highlighttext>Python</highlighttext> experience"},
            },
            {"id": "2", "name": "Invalid Snippet Vacancy", "snippet": "not_a_dict"},
            {"id": "3", "name": "Invalid Requirement Vacancy", "snippet": {"requirement": ["not", "a", "string"]}},
        ]
    }
    mock_get.return_value = mock_response
    api = HeadhunterAPI()
    keyword = "Developer"
    pages = 1
    per_page = 5

    # Act
    vacancies = api.get_vacancies(keyword, pages, per_page)

    # Assert
    expected_vacancies = [
        {"id": "1", "name": "Valid Vacancy", "snippet": {"requirement": "Python experience"}},
        {"id": "2", "name": "Invalid Snippet Vacancy", "snippet": "not_a_dict"},
        {"id": "3", "name": "Invalid Requirement Vacancy", "snippet": {"requirement": ["not", "a", "string"]}},
    ]
    assert vacancies == expected_vacancies
