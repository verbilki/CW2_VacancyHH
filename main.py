from src.file_json import JSONFunc
from src.hh_api import HeadhunterAPI
from src.user_ui import (get_query_params, get_top_vacancies, print_vacancies)
from src.vacancy import Vacancy


def user_ui() -> None:
    print("Добро пожаловать в приложение 'Vacancy APP' по работе с вакансиями HeadHunter!")

    file_path = input(
        "Введите путь к файлу для сохранения вакансий (по-умолчанию 'data/vacancies.json'): "
    )
    if not file_path:
        file_path = "data/vacancies.json"

    vacancies_list = Vacancy.cast_to_object_list(JSONFunc(file_path).get_data())
    if vacancies_list:
        print_vacancies(vacancies_list)
        print(f"Загружено {len(vacancies_list)} вакансии(й) из файла {file_path}.")

    while True:
        print("\nВыберите действие:")
        print("1. Получение вакансий из API Headhunter по ключевому слову")
        print("2. Отобрать Top N вакансий по набору слов и с ограничением по минимальной зарплате")
        print("3. Отобрать вакансии по зарплате")
        print("4. Удалить вакансию по номеру")
        print("5. Сохранить результат отбора в JSON-файл")
        print("6. Выход")

        choice = input("Введите номер действия: ").strip()

        if choice == "1":  # Получение вакансий из API Headhunter по ключевому слову
            keyword, pages, per_page = get_query_params()
            api = HeadhunterAPI()
            vacancies = api.get_vacancies(keyword, pages, per_page)
            # for vacancy in vacancies:
            #     print(vacancy)
            vacancies_list = Vacancy.cast_to_object_list(vacancies)
            json_saver = JSONFunc(file_path)
            json_saver.add_vacancies(vacancies_list)
            print_vacancies(vacancies_list)

        elif choice in ("2", "3") and not vacancies_list:
            print("Необходимо сначала выполнить действие 1.")
            continue

        elif choice == "2":  # Отобрать Top N вакансий по набору слов и с ограничением по минимальной зарплате
            get_top_vacancies(vacancies_list)

        elif choice == "4":  # 4. Удалить вакансию по номеру
            pass

        elif choice == "5":  # 5. Сохранить результат отбора в JSON-файл
            pass

        elif choice == "6":
            print("Выход из приложения. До свидания !")
            break

        else:
            print("Ошибка: выберите корректный номер действия.")


if __name__ == "__main__":
    user_ui()
