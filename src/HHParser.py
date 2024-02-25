from pprint import pprint

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

    def get_employers(self):
        params = {'sort_by': 'by_vacancies_open'}
        data = self.get_request('employers', params)
        employers = []
        for employer in data:
            employers.append({'id': employer['id'], 'name': employer['name']})

        return employers

    def get_employer_vacancies(self, employer_id):
        params = {'employer_id': employer_id}
        return self.get_request('vacancies', params)

    def get_all_vacancies(self):
        employers = self.get_employers()
        data = []
        vacancies = []
        for employer in employers:
            data.extend(self.get_employer_vacancies(employer['id']))

        for vacancy in data:
            if not vacancy['salary']:
                salary_from = 0
                salary_to = 0

            else:
                salary_from = vacancy['salary']['from'] if vacancy['salary']['from'] else 0
                salary_to = vacancy['salary']['to'] if vacancy['salary']['to'] else 0

            vacancies.append({'id': vacancy['id'],
                              'name': vacancy['name'],
                              'salary_from': salary_from,
                              'salary_to': salary_to,
                              'url': vacancy['alternate_url'],
                              'area': vacancy['area']['name'],
                              'employer': vacancy['employer']['id'],
                              'published_at': vacancy['published_at']
                              })

        return vacancies


if __name__ == '__main__':
    hh = HHParser()
    pprint(hh.get_employers(), sort_dicts=False)
