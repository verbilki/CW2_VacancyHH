import re
from typing import List, Optional

import requests

from src.base_api import ParserAPI


class HeadhunterAPI(ParserAPI):
    """
    Класс для работы с API HeadHunter (api.hh.ru)
    """

    def __init__(self) -> None:
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 2, "per_page": 5}
        self.__vacancies: List = []

    def _get_response(self, keyword: str, pages: int, per_page: int) -> Optional[requests.Response]:
        """
        Sends a GET request to the HeadHunter API to retrieve vacancies based
        on the specified keyword, page number, and number of results per page.

        Parameters:
        keyword (str): The search term to filter vacancies.
        pages (int): The page number to retrieve.
        per_page (int): The number of vacancies to retrieve per page.

        Returns:
        Optional[requests.Response]: The response object from the API if the request is successful, otherwise None.
        """
        self.__params["text"] = keyword
        self.__params["page"] = pages
        self.__params["per_page"] = per_page
        response = None

        try:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f"Возникла непредвиденная ошибка - {e}")
        finally:
            return response

    def get_vacancies(self, keyword: str, pages: int, per_page: int) -> List:
        """
        Retrieves vacancies from the HeadHunter API based on the specified keyword,
        page number, and number of results per page.

        Parameters:
        keyword (str): The search term to filter vacancies.
        pages (int): The number of pages to retrieve.
        per_page (int): The number of vacancies to retrieve per page.

        Returns:
        List: A list of retrieved vacancies.
        """
        all_vacancies = []
        for page in range(pages):
            response = self._get_response(keyword, page, per_page)
            if response:
                try:
                    vacancies = response.json().get("items", [])
                except ValueError as e:
                    print(f"Error parsing JSON response: {e}")
                    continue

                for vacancy in vacancies:
                    for field in ["snippet"]:
                        if (
                            field in vacancy and isinstance(vacancy[field], dict) and "requirement" in vacancy[field]
                        ) and isinstance(vacancy[field]["requirement"], str):
                            vacancy[field]["requirement"] = self.remove_highlight_tags(vacancy[field]["requirement"])

                all_vacancies.extend(vacancies)
            else:
                print(f"No response received for page {page}")

        return all_vacancies

    @staticmethod
    def remove_highlight_tags(text: str) -> str:
        """
        Removes HTML tags from the specified text that highlight search query words in the text.

        Parameters:
        text (str): The text to remove HTML tags from.

        Returns:
        str: The text with the HTML tags removed.
        """
        return re.sub(r"<highlighttext>|</highlighttext>", "", text)


if __name__ == "__main__":
    api = HeadhunterAPI()
    keyword = input("Введите ключевое слово для поиска вакансий: ")
    pages = int(input("Введите количество страниц для поиска: "))
    per_page = int(input("Введите количество вакансий на странице: "))
    vacancies = api.get_vacancies(keyword, pages, per_page)
    print(vacancies)
