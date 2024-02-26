import requests


class HHParser:
    @staticmethod
    def get_request(api_word: str, extra_params: dict = None) -> list[dict]:
        headers = {"HH-User-Agent": "Kursovaya/1.0 (vavilon164@yandex.ru)"}
        params = {"per_page": 10}
        if extra_params:
            params.update(extra_params)

        response = requests.get(f'https://api.hh.ru/{api_word}/', params=params, headers=headers)

        if response.status_code == 200:
            return response.json()["items"]

        return [{'Ошибка': f'{response.status_code}'}]

    def get_employers(self, extra_params: dict = None):
        params = {'sort_by': 'by_vacancies_open'}
        if extra_params:
            params.update(extra_params)

        data = self.get_request('employers', params)
        employers = []
        for employer in data:
            employers.append({'id': employer['id'], 'name': employer['name']})

        return employers

    def get_employer_vacancies(self, employer_id, extra_params: dict = None):
        params = {'employer_id': employer_id}
        if extra_params:
            params.update(extra_params)

        return self.get_request('vacancies', params)

    def get_all_vacancies(self, employers: list[dict], extra_params: dict = None):
        vacancies = []
        for employer in employers:
            vacancies.extend(self.get_employer_vacancies(employer['id'], extra_params))

        return vacancies

    @staticmethod
    def sort_vacancies(vacancies: list[dict]):
        sorted_vacancies = []
        for vacancy in vacancies:
            if not vacancy['salary']:
                salary_from = 0
                salary_to = 0

            else:
                salary_from = vacancy['salary']['from'] if vacancy['salary']['from'] else 0
                salary_to = vacancy['salary']['to'] if vacancy['salary']['to'] else 0

            sorted_vacancies.append({'id': vacancy['id'],
                                     'name': vacancy['name'],
                                     'salary_from': salary_from,
                                     'salary_to': salary_to,
                                     'url': vacancy['alternate_url'],
                                     'area': vacancy['area']['name'],
                                     'employer': vacancy['employer']['id'],
                                     'published_at': vacancy['published_at']
                                     })

        return sorted_vacancies
