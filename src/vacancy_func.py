from typing import List


def filter_vacancies(vacancies: List, filter_words: str) -> List:
    """
    This function filters a list of vacancies by a given keyword.

    Parameters:
    vacancies (List): List of Vacancy objects.
    filter_words (str): A keyword to filter vacancies by.

    Returns:
    List: A list of Vacancy objects that match the filter.
    """
    filtered_vacancies = []
    for vacancy in vacancies:
        if filter_words in vacancy.description:
            filtered_vacancies.append(vacancy)

    return filtered_vacancies


def get_vacancies_by_salary(vacancies: List, salary: int) -> List:
    """
    This function filters a list of vacancies by a given salary threshold.

    Parameters:
    vacancies (List): List of Vacancy objects.
    salary (int): Salary threshold to filter vacancies by.

    Returns:
    List: A list of Vacancy objects that have a salary greater than the given threshold.
    """
    ranged_vacancies = []
    for vacancy in vacancies:
        if vacancy.salary > salary:
            ranged_vacancies.append(vacancy)

    return ranged_vacancies


def sort_vacancies(vacancies: List) -> List:
    """
    Sort a list of vacancies by their salary in ascending order.

    Parameters:
    vacancies (List): List of Vacancy objects.

    Returns:
    List: A sorted list of Vacancy objects.
    """
    return sorted(vacancies, key=lambda x: x.salary)


def get_top_vacancies(vacancies: List, top_n: int = 10) -> List:
    """
    Return the top N vacancies from a list of vacancies.

    Parameters:
    vacancies (List): A list of Vacancy objects.
    top_n (int): The number of top vacancies to return. Defaults to 10.

    Returns:
    List: A list of the top N Vacancy objects.
    """
    if top_n > len(vacancies):
        top_n = len(vacancies)

    return vacancies[:top_n]


def print_vacancies(vacancies: List) -> None:
    """
    Prints a list of Vacancy objects.

    Parameters:
    top_vacancies (List): A list of Vacancy objects to print.

    Returns: None
    """
    for vacancy in vacancies:
        print(vacancy)


if __name__ == "__main__":
    pass
