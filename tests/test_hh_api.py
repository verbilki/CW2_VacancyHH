from unittest.mock import Mock, patch

import requests

from src.hh_api import HH_API


@patch("requests.get")
def test_get_response_valid_parameters(mock_get):
    # Arrange
    mock_response = Mock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    api = HH_API()
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
def test_get_response_raises_exception_on_404(mock_get):
    # Arrange
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    api = HH_API()
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
def test_get_response_raises_exception_on_500(mock_get):
    # Arrange
    mock_response = Mock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response
    api = HH_API()
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
def test_get_response_handles_unreachable_api(mock_get):
    # Arrange
    mock_get.side_effect = requests.exceptions.ConnectionError
    api = HH_API()
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
def test_get_response_sets_correct_text_parameter(mock_get):
    # Arrange
    mock_response = Mock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    api = HH_API()
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
def test_get_response_handles_empty_keyword(mock_get):
    # Arrange
    mock_response = Mock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    api = HH_API()
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
def test_get_response_handles_large_page_and_per_page(mock_get):
    # Arrange
    mock_response = Mock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    api = HH_API()
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
def test_get_response_invalid_url_prints_error_message(mock_get):
    # Arrange
    mock_get.side_effect = requests.exceptions.InvalidURL
    api = HH_API()
    keyword = "Python Developer"
    page = 1
    per_page = 5

    # Act
    with patch("builtins.print") as mock_print:
        api._get_response(keyword, page, per_page)

    # Assert
    mock_print.assert_called_once_with("Возникла непредвиденная ошибка - ")
