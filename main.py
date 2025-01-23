from src.file_json import JSONFunc
from src.hh_api import HeadhunterAPI
from src.user_ui import (initial_load, get_query_params, get_top_vacancies, delete_vacancy_by_id, print_vacancies)
from src.vacancy import Vacancy

def user_ui() -> None:
    vacancies_file_path, vacancies_processed = initial_load()

    while True:
        print("\nВыберите действие:")
        print("1. Получение вакансий из API Headhunter по ключевому слову")
        print("2. Отобрать Top N вакансий по набору слов и с ограничением по минимальной зарплате")
        print("3. Отобрать вакансии по ключевому(ым) слову(ам) в описании")
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

        elif choice == "3":  # 3. Отобрать вакансии по ключевому(ым) слову(ам) в описании
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
