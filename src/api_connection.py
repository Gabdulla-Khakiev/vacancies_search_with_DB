from abc import ABC, abstractmethod
import requests


class HeadHunter(ABC):
    @abstractmethod
    def __init__(self):
        pass


class LoadVacancies(HeadHunter):
    """
    Класс для получения вакансий с HH с помощью Api ключа
    """

    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'area': 113, 'page': 0, 'per_page': 100}
        self.vacancies = []

    def connect(self):
        """
        Проверяет доступность API HeadHunter.

        :return: True, если подключение успешно; False в противном случае.
        """
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()  # Проверка на успешный ответ
            return True  # Успешное подключение
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при подключении к API: {e}")

            return False  # Ошибка подключения

    def get_vacancies(self, keyword: str):
        """
        Загружает вакансии с сайта HeadHunter по ключевому слову.

        :param keyword: Ключевое слово для поиска вакансий.
        """
        self.params['text'] = keyword

        try:
            while self.params.get('page') < 20:
                response = requests.get(self.url, headers=self.headers, params=self.params)
                response.raise_for_status()  # Проверка на наличие ошибок

                vacancies = response.json().get('items')
                if not vacancies:
                    break

                self.vacancies.extend(vacancies)
                self.params['page'] += 1

        except requests.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
            return []

    def get_vacancies_by_employer_id(self, employer_id):
        try:
            self.params["employer_id"] = employer_id
            while self.params.get('page') < 20:
                response = requests.get(self.url, headers=self.headers, params=self.params)
                response.raise_for_status()  # Проверка на наличие ошибок

                vacancies = response.json().get('items')
                if not vacancies:
                    break

                self.vacancies.extend(vacancies)
                self.params['page'] += 1

        except requests.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
            return []


class FindEmployerFromHH(HeadHunter):
    """
    Класс для получения вакансий с HH с помощью Api ключа
    """
    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'area': 113, 'page': 0, 'per_page': 100, 'sort_by': 'by_vacancies_open'}
        self.employers = []

    def __get_employer_info(self, keyword=""):
        """
        Загружает инфо-ию по работодателям с сайта HeadHunter по ключевому слову.

        :param keyword: Ключевое слово для поиска вакансий.
        """

        self.params['text'] = keyword

        try:
            while self.params.get('page') < 20:
                response = requests.get(self.url, headers=self.headers, params=self.params)
                response.raise_for_status()  # Проверка на наличие ошибок

                employers = response.json().get('items')
                if not employers:
                    break

                self.employers.extend(employers)
                self.params['page'] += 1

        except requests.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
            return []

    def get_employer_info(self, employer_count, keyword=''):
        self.__get_employer_info(keyword)
        for employer in self.employers[:employer_count]:
            print(f"{employer.get('name')}, id: {employer.get('id')}")
        print('...')
        return self.employers


if __name__ == "__main__":
    pass
