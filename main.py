from src.hh_api import HeadhunterAPI
from src.user_ui import (get_query_params)

def user_ui() -> None:
    print("Добро пожаловать в приложение 'Vacancy APP' по работе с вакансиями HeadHunter!")

    file_path = input(
        "Введите путь к файлу для сохранения вакансий (по-умолчанию 'data/vacancies.json'): "
    )
    if not file_path:
        file_path = "data/vacancies.json"

    while True:
        print("\nВыберите действие:")
        print("1. Отбор вакансий по ключевому слову")
        print("2. Отобрать Top N вакансий по зарплате")
        print("3. Отобрать вакансии по зарплате")
        print("4. Сохранить результат фильтрации в JSON-файл")
        print("5. Выход")

        choice = input("Введите номер действия: ").strip()

        if choice == "1":
            keyword, pages, per_page = get_query_params()
            api = HeadhunterAPI()
            vacancies = api.get_vacancies(keyword, pages, per_page)
            for vacancy in vacancies:
                print(vacancy)

        elif choice == "2":
            pass

        elif choice == "3":
            pass

        elif choice == "4":
            pass

        elif choice == "5":
            print("Выход из приложения. До свидания !")
            break

        else:
            print("Ошибка: выберите корректный номер действия.")


if __name__ == "__main__":
    user_ui()
