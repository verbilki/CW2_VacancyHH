
def get_query_params() -> tuple[str, int, int]:
    user_query = input("Введите ключевое слово для отбора вакансий (по умолчанию: 'Python'): ").strip()
    if not user_query:
        user_query = 'Python'

    per_page = input("Введите количество вакансий на странице(максимум=100, по-умолчанию=10): ").strip()
    per_page = int(per_page) if per_page.isdigit() and 1 <= int(per_page) <= 100 else 10
    pages = input("Количество страниц (не более 10): ").strip()
    pages = int(pages) if pages.isdigit() and 1 <= int(pages) <= 10 else 1

    return user_query, pages, per_page

