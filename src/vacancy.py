from typing import Any, Dict, List


class Vacancy:
    """Класс для работы с вакансиями"""

    __slots__ = ("vacancy_id", "name", "url", "description", "salary")

    def __init__(self, vacancy_id: str, name: str, url: str, description: str, salary: int) -> None:
        self.vacancy_id = self.__validate_id(vacancy_id)
        self.name = self.__validate_name(name)
        self.url = self.__validate_url(url)
        self.description = self.__validate_description(description)
        self.salary = self.__validate_salary(salary)

    def __str__(self) -> str:
        return (
            f"Номер: {self.vacancy_id}. Название: {self.name}. "
            f"Зарплата: {self.salary}. Ссылка на вакансию: {self.url}. "
            f"Описание: {self.description.replace('\u2060', '')}"
        )

    @staticmethod
    def __validate_id(vacancy_id: str) -> str:
        if not isinstance(vacancy_id, str) or not vacancy_id.isdigit():
            raise ValueError("Invalid id")
        return vacancy_id

    @staticmethod
    def __validate_name(name: str) -> str:
        if not isinstance(name, str) or not name:
            raise ValueError("Invalid name")
        return name

    @staticmethod
    def __validate_url(url: str) -> str:
        if not isinstance(url, str) or not url.startswith("http"):
            raise ValueError("Invalid URL")
        return url

    @staticmethod
    def __validate_description(description: str) -> str:
        if not isinstance(description, str):
            raise ValueError("Недопустимое описание вакансии")
        return description[:1000]

    @staticmethod
    def __validate_salary(salary: int) -> int:
        if salary is None:
            return 0
        elif not (isinstance(salary, int) or isinstance(salary, float)) or salary < 0:
            raise ValueError("Invalid salary_min")
        return salary

    @staticmethod
    def salary_data(vacancy: Dict) -> Any:
        if vacancy["salary"] is None:
            return 0
        elif vacancy["salary"]["from"] and vacancy["salary"]["to"] is None:
            return vacancy["salary"]["from"]
        elif vacancy["salary"]["from"] is None and vacancy["salary"]["to"]:
            return vacancy["salary"]["to"]
        else:
            return (vacancy["salary"]["to"] + vacancy["salary"]["from"]) / 2

    @classmethod
    def cast_to_object_list(cls, hh_vacancies: List) -> List:
        """
        Casts a list of dictionaries to a list of Vacancy objects.

        Args:
        hh_vacancies (List): A list of dictionaries representing vacancies as returned by HeadHunter API.

        Returns:
        List: A list of Vacancy objects, with each object containing the following attributes:
            vacancy_id (str): The id of the vacancy.
            name (str): The name of the vacancy.
            url (str): The URL of the vacancy.
            description (str): The description of the vacancy.
            salary (int): The salary of the vacancy.

        Raises:
        ValueError: If the salary is invalid, the method will catch the ValueError and print an error message.
        """
        vacancy_objects = []
        for vacancy in hh_vacancies:
            try:
                salary = cls.salary_data(vacancy)

                vacancy = cls(
                    vacancy_id=vacancy.get("id"),
                    name=vacancy.get("name"),
                    url=vacancy.get("alternate_url"),
                    description=vacancy.get("snippet", {}).get("requirement", ""),
                    salary=round(salary),
                )
                vacancy_objects.append(vacancy)
            except ValueError as e:
                print(f"Skipping invalid vacancy: {e}")
        return vacancy_objects

    def __eq__(self, other: object) -> bool:
        """
        Checks if two Vacancy objects have equal salaries.

        Args:
        other (object): The object to compare with.

        Returns:
        bool: True if the salaries are equal, False otherwise.

        Raises:
        NotImplementedError: If the object is not an instance of Vacancy.
        """
        if isinstance(other, Vacancy):
            return self.salary == other.salary
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        """
        Checks if the salary of the current Vacancy object is less than the salary of another Vacancy object.

        Args:
        other (object): The object to compare with.

        Returns:
        bool: True if the salary of the current object is less than the salary of the other object, False otherwise.

        Raises:
        NotImplementedError: If the object is not an instance of Vacancy.
        """
        if isinstance(other, Vacancy):
            return self.salary < other.salary
        return NotImplemented

    def __le__(self, other: object) -> bool:
        """
        Checks if the salary of the current Vacancy object is less than or equal
        to the salary of another Vacancy object.

        Args:
        other (object): The object to compare with.

        Returns:
        bool: True if the salary of the current object is less than or equal
        to the salary of the other object, False otherwise.

        Raises:
        NotImplementedError: If the object is not an instance of Vacancy.
        """
        if isinstance(other, Vacancy):
            return self.salary <= other.salary
        return NotImplemented

    def __gt__(self, other: object) -> bool:
        """
        Checks if the salary of the current Vacancy object is greater than the salary of another Vacancy object.

        Args:
        other (object): The object to compare with.

        Returns:
        bool: True if the salary of the current object is greater than the salary of the other object, False otherwise.

        Raises:
        NotImplementedError: If the object is not an instance of Vacancy.
        """
        if isinstance(other, Vacancy):
            return self.salary > other.salary
        return NotImplemented

    def __ge__(self, other: object) -> bool:
        """
        Checks if the salary of the current Vacancy object is greater than or equal
        to the salary of another Vacancy object.

        Args:
        other (object): The object to compare with.

        Returns:
        bool: True if the salary of the current object is greater than or equal
        to the salary of the other object, False otherwise.

        Raises:
        NotImplementedError: If the object is not an instance of Vacancy.
        """
        if isinstance(other, Vacancy):
            return self.salary >= other.salary
        return NotImplemented

    def __repr__(self) -> str:
        """
        Returns a string representation of the Vacancy object.

        The string representation is of the form "Vacancy(title=<name>, salary=<salary>)".

        Returns:
        str: A string representation of the Vacancy object.
        """
        return f"{self.__class__.__name__}(title={self.name}, salary={self.salary})"
