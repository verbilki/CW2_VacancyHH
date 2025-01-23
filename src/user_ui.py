import os

from dotenv import load_dotenv

from src.file_json import JSONFunc
from src.vacancy import Vacancy

prj_root = os.path.dirname(os.path.dirname(__file__))


def initial_load() -> tuple[str, list]:
    """
    Load vacancies from a JSON file and return the file path and list of vacancies.

    This function prompts the user to input a file path for loading vacancies.
    If no input is provided, it defaults to the file path specified in the environment variables.
    It attempts to load vacancies from the specified JSON file, converts them into Vacancy objects,
    and prints the loaded vacancies. If the file is not found, it returns an empty list of vacancies.

    Returns:
    tuple: A tuple containing the file path (str) and a list of Vacancy objects (list).
    """
    print("Добро пожаловать в приложение 'Vacancy APP' по работе с вакансиями HeadHunter!")
    load_dotenv()

    file_path_input = input(
        f"Введите путь к JSON-файлу от корня приложения для загрузки вакансий "
        f"(Enter = '{os.getenv('FILEPATH')}.json'): "
    ).strip()

    if file_path_input:
        vacancies_file_path = os.path.join(prj_root, file_path_input)
    else:
        vacancies_file_path = os.path.join(prj_root, os.getenv("FILEPATH", "data/vacancies"), ".json")

    if os.path.exists(vacancies_file_path):
        vacancies_loaded = Vacancy.cast_to_object_list(JSONFunc(vacancies_file_path).get_data())
        print_vacancies(vacancies_loaded)
        print(f"Загружено {len(vacancies_loaded)} вакансии(й) из файла {vacancies_file_path.replace(prj_root, '')}.")
    else:
        vacancies_loaded = []
        print(f"Файл {vacancies_file_path.replace(prj_root, '')} не найден. Выберите в меню пункт 1.")

    return vacancies_file_path, vacancies_loaded


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

    per_page_input = input("Введите количество вакансий на странице(максимум = 40, Enter = 10): ").strip()
    per_page = int(per_page_input) if per_page_input.isnumeric() and 1 <= int(per_page_input) <= 40 else 10
    pages_input = input("Количество страниц (не более 10: Enter = 3): ").strip()
    pages = int(pages_input) if pages_input.isnumeric() and 1 <= int(pages_input) <= 10 else 3

    return user_query, pages, per_page


def get_top_vacancies(vacancies: list) -> list:
    """
    Get the top N vacancies filtered by keywords and salary.

    Parameters:
    vacancies (list[Vacancy]): The list of vacancies to filter.

    Returns:
    list[Vacancy]: The list of top N vacancies.

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
        return vacancies

    if top_n > len(filtered_by_keywords) or top_n == 0:
        top_n = len(filtered_by_keywords)
    print(f"Top-{top_n} вакансий (отсортированных по убыванию зарплат):")
    result_list = sorted(filtered_by_keywords, key=lambda x: x.salary, reverse=True)[:top_n]
    print_vacancies(result_list)
    return result_list


def delete_vacancy_by_id(vacancies: list) -> None:
    """
    Delete a vacancy from a list of vacancies by its ID.

    Parameters:
    vacancies (list): A list of Vacancy objects.

    Returns: None.
    """
    id_input = input("Введите номер вакансии для удаления: ").strip()
    if not id_input.isnumeric():
        print("Некорректный ввод. ID вакансии должен быть числом.")
        return

    is_found = False

    for vacancy in vacancies:
        if vacancy.vacancy_id == id_input:
            vacancies.remove(vacancy)
            print(f"Удалена следующая вакансия:\n {vacancy}")
            is_found = True
            break

    if not is_found:
        print(f"Вакансия с номером {id_input} не найдена.")


def print_vacancies(vacancies: list) -> None:
    """
    Prints a list of Vacancy objects.

    Parameters:
    vacancies (list): A list of Vacancy objects to print.

    Returns: None
    """
    for i, vacancy in enumerate(vacancies, 1):
        print(f"{i}. {vacancy}")
