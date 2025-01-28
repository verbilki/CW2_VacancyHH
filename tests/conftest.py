import pytest

from src.vacancy import Vacancy


@pytest.fixture
def vacancies_fixture_1() -> list[Vacancy]:
    return [
        Vacancy("100", "Software Engineer", "https://promo1.com", "Software Engineer with Python experience", 100_000),
        Vacancy("200", "Data Scientist", "https://promo2.com", "Data Scientist with machine learning skills", 120_000),
        Vacancy("300", "Frontend Developer", "https://promo3.com", "Frontend Developer with React knowledge", 80_000),
        Vacancy("400", "Java Developer", "https://promo4.com", "Java Developer with Spring framework", 90_000),
    ]


@pytest.fixture
def vacancies_fixture_2() -> list[Vacancy]:
    return [
        Vacancy(
            "500", "C++ Developer", "https://promo5.com", "C++ Developer with experience in Qt framework", 140_000
        ),
        Vacancy("600", "Python Developer", "https://promo6.com", "Python Developer with Django experience", 150_000),
        Vacancy("700", "Java Developer", "https://promo7.com", "Java Developer with Spring framework", 130_000),
        Vacancy("800", "C# Developer", "https://promo8.com", "C# Developer with .NET Core experience", 110_000),
    ]
