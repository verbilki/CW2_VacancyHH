from src.file_json import JSONFunc
from src.hh_api import HeadhunterAPI
from src.user_ui import (get_query_params, get_top_vacancies, delete_vacancy_by_id, print_vacancies)
from src.vacancy import Vacancy
from dotenv import load_dotenv
import os

prj_root = os.path.dirname(__file__)
def user_ui() -> None:
    print("Добро пожаловать в приложение 'Vacancy APP' по работе с вакансиями HeadHunter!")

    load_dotenv()
    vacancies_file_path = os.path.join(prj_root, os.getenv("FILEPATH") + ".json")

    file_path_input = input(
        f"Введите путь к файлу для загрузки вакансий (Enter = '{os.getenv('FILEPATH')}.json'): "
    ).strip()
    if not file_path_input:
        vacancies_file_path = os.getenv('FILEPATH') + ".json"

    if os.path.exists(vacancies_file_path):
        vacancies_processed = Vacancy.cast_to_object_list(JSONFunc(vacancies_file_path).get_data())
        print_vacancies(vacancies_processed)
        print(f"Загружено {len(vacancies_processed)} вакансии(й) из файла {vacancies_file_path.replace(prj_root, '')}.")
    else:
        print(f"Файл {vacancies_file_path.replace(prj_root, '')} не найден. Выберите в меню пункт 1.")
        vacancies_processed = []

    while True:
        print("\nВыберите действие:")
        print("1. Получение вакансий из API Headhunter по ключевому слову")
        print("2. Отобрать Top N вакансий по набору слов и с ограничением по минимальной зарплате")
        print("3. Исключить вакансии по ключевым словам")
        print("4. Удалить вакансию по номеру")
        print("5. Сохранить результат отбора в JSON-файл")
        print("6. Выход")

        choice = input("Введите номер действия: ").strip()

        if choice == "1":  # Получение вакансий из API Headhunter по ключевому слову
            keyword, pages, per_page = get_query_params()
            vacancies = HeadhunterAPI().get_vacancies(keyword, pages, per_page)
            vacancies_processed = Vacancy.cast_to_object_list(vacancies)
            json_saver = JSONFunc(vacancies_file_path)
            json_saver.add_vacancies(vacancies_processed)
            print_vacancies(vacancies_processed)

        elif choice in ("2", "3", "4", "5") and not vacancies_processed:
            print("Необходимо сначала выполнить действие 1.")
            continue

        elif choice == "2":  # Отобрать Top N вакансий по набору слов и с ограничением по минимальной зарплате
            vacancies_processed = get_top_vacancies(vacancies_processed)

        elif choice == "3":  # 3. Исключить вакансии по ключевым словам
            pass

        elif choice == "4":  # 4. Удалить вакансию по номеру
            delete_vacancy_by_id(vacancies_processed)

        elif choice == "5":  # 5. Сохранить результат отбора в JSON-файл
            JSONFunc(vacancies_file_path).add_vacancies(vacancies_processed)

        elif choice == "6":
            print("Выход из приложения. До свидания !")
            break

        else:
            print("Ошибка: выберите корректный номер действия.")


if __name__ == "__main__":
    user_ui()
