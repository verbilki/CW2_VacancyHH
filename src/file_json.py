import json
import os
from typing import Any, List

from src.base_files import Files


class JSONFunc(Files):
    def __init__(self, file_path: str) -> None:
        self.__file_path = file_path

    def get_data(self) -> Any:
        """
        Retrieves the list of existing vacancies from the JSON file.

        This method checks if the specified file path exists. If it does, it attempts to load
        and return the list of vacancies from the file. If the file is empty or contains
        invalid JSON, an empty list is returned. If the file does not exist, an empty list
        is also returned.

        Returns:
        Any: A list of existing vacancies, or an empty list if the file is not found or is invalid.
        """
        existing_vacancies = []

        if os.path.exists(self.__file_path):
            with open(self.__file_path, "r+", encoding="utf-8") as f:
                try:
                    existing_vacancies = json.load(f)

                except json.JSONDecodeError:
                    pass
                finally:
                    return existing_vacancies
        else:
            return existing_vacancies

    def add_vacancies(self, vacancies: List) -> None:
        """
        Adds new vacancies to the existing list of vacancies in the JSON file.

        This method retrieves the current list of vacancies, checks for any duplicate
        vacancies by their ID, and appends new vacancies to the list if they do not
        already exist. Finally, it saves the updated list back to the JSON file.

        Args:
        vacancies (List): A list of Vacancy objects to be added.

        Returns: None
        """
        existing_vacancies = self.get_data()
        existing_vacancies_dict = {vacancy["id"]: vacancy for vacancy in existing_vacancies}

        for vacancy in vacancies:
            if vacancy.vacancy_id in existing_vacancies_dict:
                continue
            existing_vacancies.append(
                {
                    "id": vacancy.vacancy_id,
                    "name": vacancy.name,
                    "url": vacancy.url,
                    "description": vacancy.description,
                    "salary": vacancy.salary,
                }
            )

        with open(self.__file_path, "w", encoding="utf-8") as f:
            json.dump(existing_vacancies, f, ensure_ascii=False, indent=4)

    def delete_vacancy(self, vacancy_id: str) -> Any:
        """
        Deletes a vacancy from the list of existing vacancies in the JSON file.

        Args:
        vacancy_id: The id of the vacancy to be deleted.

        Returns:
        List: A list of remaining vacancies.
        """
        existing_vacancies = self.get_data()
        if not existing_vacancies:
            return []

        for index, vacancy in enumerate(existing_vacancies):
            if vacancy_id in vacancy.values():
                existing_vacancies.pop(index)
                with open(self.__file_path, "w", encoding="utf-8") as file:
                    json.dump(existing_vacancies, file, ensure_ascii=False, indent=4)
                break
