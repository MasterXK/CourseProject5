from pprint import pprint

import psycopg2
from config import config


class DBManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def execute_query(self, query) -> list:
        """
        Функция выполняет SQL-запрос. Возвращает результат запроса.
        """
        conn = psycopg2.connect(dbname=self.db_name, **config())
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()

        conn.close()

        return result

    def get_companies_and_vacancies_count(self):
        """
        Функция получает список всех компаний и количество вакансий у каждой компании
        :return:
        """
        companies_count = self.execute_query('SELECT COUNT(*) FROM employers')[0][0]
        vacancies_count = self.execute_query('SELECT COUNT(*) FROM vacancies')[0][0]

        return f'Кол-во компаний: {companies_count}\nКол-во вакансий: {vacancies_count}'

    def get_all_vacancies(self):
        """
        Функция получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        :return:
        """
        vacancies = [('id', 'name', 'area', 'salary_from', 'salary_to', 'url', 'published_at', 'employer')]
        vacancies.extend(self.execute_query('SELECT * FROM vacancies'))

        return vacancies

    def get_avg_salary(self):
        """
        Функция получает среднюю зарплату по вакансиям
        :return:
        """
        avg_salary = self.execute_query('SELECT AVG(round((salary_from + salary_to) / 2)) FROM vacancies')

        return avg_salary[0][0]

    def get_vacancies_with_higher_salary(self):
        """
        Функция получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        :return:
        """
        avg_salary = self.get_avg_salary()

        vacancies = self.execute_query(f'SELECT * FROM vacancies '
                                       f'WHERE round((salary_from + salary_to) / 2) > {avg_salary}')

        return vacancies

    def get_vacancies_with_keyword(self, keywords: list | str):
        """
        Функция получает список всех вакансий, в названии которых содержатся переданные в метод слова
        :return:
        """
        vacancies = []
        if type(keywords) is list:
            for keyword in keywords:
                vacancies.extend(self.execute_query(f'SELECT * FROM vacancies '
                                                    f'WHERE name LIKE \'%{keyword}%\''))
        else:
            for keyword in keywords.split():
                vacancies.extend(self.execute_query(f'SELECT * FROM vacancies '
                                                    f'WHERE name LIKE \'%{keyword}%\''))

        return vacancies


if __name__ == '__main__':
    db_mng = DBManager('course_work_5')
    print(db_mng.get_vacancies_with_keyword('Специалист'))
    # for vacancy in db_mng.get_all_vacancies():
    #     print(vacancy)
