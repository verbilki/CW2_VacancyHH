from abc import ABC, abstractmethod
from typing import List, Optional

import requests


class API_Parser(ABC):
    """Абстрактный класс для работы с API api.hh.ru"""

    @abstractmethod
    def _get_response(self, keyword: str, page: int, per_page: int) -> Optional[requests.Response]:
        """
        Abstract method to connect to the job vacancies API using a keyword.

        Parameters:
        keyword (str): The search term used to query the API for job vacancies.
        page (int): The page number of the results to retrieve.
        per_page (int): The number of results to retrieve per page.

        Returns:
        Optional[requests.Response]: The response object from the API call, or None if the request fails.
        """
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str, page: int, per_page: int) -> List:
        """Абстрактный метод для преобразования отклика с API в списочный объект Python"""
        pass
