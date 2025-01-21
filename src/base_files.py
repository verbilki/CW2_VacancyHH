from abc import ABC, abstractmethod
from typing import List


class Files(ABC):
    @abstractmethod
    def get_data(self) -> List:
        pass

    @abstractmethod
    def add_vacancies(self, hh_vacancies: List) -> None:
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id: str) -> List | None:
        pass
