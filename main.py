from src.hh_api import HH_API

if __name__ == "__main__":
    api = HH_API()
    keyword = input("Введите ключевое слово для поиска вакансий: ")
    pages = int(input("Введите количество страниц для поиска: "))
    per_page = int(input("Введите количество вакансий на странице: "))
    vacancies = api.get_vacancies(keyword, pages, per_page)
    print(vacancies)
