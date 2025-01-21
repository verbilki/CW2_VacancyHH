def get_query_params() -> tuple[str, int, int]:
    """
    Get query parameters from the user.

    Parameters:
    None

    Returns:
    tuple: A tuple of three parameters: user_query (str), pages (int), per_page (int).

    The function prompts the user to enter a keyword and the number of pages and items per page.
    If the user does not enter anything, the default values are used.
    The function then returns a tuple containing the entered keyword,
    the number of pages, and the number of items per page.
    """
    user_query = input("Введите ключевое слово для отбора вакансий (Enter: 'Python'): ").strip()
    if not user_query:
        user_query = "Python"

    per_page_input = input("Введите количество вакансий на странице(максимум = 100, Enter = 10): ").strip()
    per_page = int(per_page_input) if per_page_input.isnumeric() and 1 <= int(per_page_input) <= 100 else 10
    pages_input = input("Количество страниц (не более 10: Enter = 1): ").strip()
    pages = int(pages_input) if pages_input.isnumeric() and 1 <= int(pages_input) <= 10 else 1

    return user_query, pages, per_page


def get_top_vacancies(vacancies: list):
    """
    Get the top N vacancies filtered by keywords and salary.

    Parameters:
    vacancies (list[Vacancy]): The list of vacancies to filter.

    Returns:
    None

    The function prompts the user to enter keywords and the lower limit of the salary.
    It then filters the vacancies by keywords and salary, sorts the filtered vacancies
    by salary in descending order, and prints the top N vacancies.
    """
    keywords = (
        input("Введите слова для фильтрации вакансий по наименованию или описанию (Enter = без фильтра): ")
        .strip()
        .split()
    )

    low_limit_salary_input = input("Введите нижний порог зарплаты (Enter = 0): ").strip()
    low_limit_salary = int(low_limit_salary_input) if low_limit_salary_input.isnumeric() else 0

    top_n_input = input("Введите количество вакансий для отбора по зарплате (Enter: все доступные): ").strip()
    top_n = int(top_n_input) if top_n_input.isnumeric() else 0

    filtered_by_salary = [vacancy for vacancy in vacancies if vacancy.salary >= low_limit_salary]
    filtered_by_keywords = []

    if keywords:
        for vacancy in filtered_by_salary:
            for keyword in keywords:
                if keyword.lower() in vacancy.name.lower() or keyword.lower() in vacancy.description.lower():
                    filtered_by_keywords.append(vacancy)
                    break
    else:
        filtered_by_keywords = filtered_by_salary

    if not filtered_by_keywords:
        print("Нет подходящих вакансий. Попробуйте изменить параметры поиска.")
        return

    if top_n > len(filtered_by_keywords) or top_n == 0:
        top_n = len(filtered_by_keywords)
    print(f"Top-{top_n} вакансий (отсортированных по убыванию зарплат):")
    print_vacancies(sorted(filtered_by_keywords, key=lambda x: x.salary, reverse=True)[:top_n])


def print_vacancies(vacancies: list) -> None:
    """
    Prints a list of Vacancy objects.

    Parameters:
    vacancies (list): A list of Vacancy objects to print.

    Returns: None
    """
    for i, vacancy in enumerate(vacancies, 1):
        print(f"{i}. {vacancy}")
