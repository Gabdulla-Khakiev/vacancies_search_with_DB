class Vacancy:
    """ Класс для представления вакансии """
    __slots__ = ('id', 'name', 'area', 'employer', 'url', 'salary', 'description')

    def __init__(self, vacancy):
        self.id = vacancy.get('id')
        self.name = vacancy.get('name')
        self.area = vacancy.get('area').get('name')
        self.employer = vacancy.get('employer').get('name')
        self.url = self.__validate_url(vacancy)
        self.salary = self.__validate_salary(vacancy)
        self.description = self.__validate_description(vacancy)

    @staticmethod
    def __validate_url(vacancy):
        if vacancy.get('response_url') is not None:
            return vacancy.get('response_url')
        else:
            return vacancy.get('apply_alternate_url')

    @staticmethod
    def __validate_description(vacancy):
        if (vacancy.get('snippet').get('requirement') is not None or
                vacancy.get('snippet') is not None):
            description = vacancy.get('snippet')
            return description
        else:
            return 'Без описания'

    @staticmethod
    def __validate_salary(vacancy):
        salary = vacancy.get('salary')
        if not salary:
            return "Зарплата не указана"
        salary_from = salary.get('from') or 0
        salary_to = salary.get('to') or 0
        return int((salary_from + salary_to) / 2) if salary_from or salary_to else "Зарплата не указана"

    def to_dict(self):
        """Преобразует объект Vacancy в словарь для сериализации в JSON."""
        return {
            'id': self.id,
            'name': self.name,
            'area': self.area,
            'employer': self.employer,
            'url': self.url,
            'salary': self.salary,
            'description': self.description
        }

    @staticmethod
    def remove_highlight_tags(description):
        """
        Убирает теги <highlighttext> из требований и обязанностей вакансии.
        """
        if isinstance(description, dict):
            for key in ['requirement', 'responsibility']:
                if description.get(key):
                    description[key] = re.sub(r'<highlighttext>|</highlighttext>', '', description[key])
        return description

    @staticmethod
    def cast_to_object_list(vacancies_data):
        """Преобразует список вакансий из JSON в список объектов Vacancy."""
        return [Vacancy(vacancy) for vacancy in vacancies_data]