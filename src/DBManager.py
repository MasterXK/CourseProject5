import psycopg2
from config import config


class DBManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def execute_query(self, query) -> list:
        """Возвращает результат запроса"""
        conn = psycopg2.connect(dbname=self.db_name, **config())
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        conn.close()

    def get_companies_and_vacancies_count(self):
        '''
        Функция получает список всех компаний и количество вакансий у каждой компании
        :return:
        '''
        pass

    def get_all_vacancies(self):
        '''
        Функция получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        :return:
        '''
        pass

    def get_avg_salary(self):
        '''
        Функция получает среднюю зарплату по вакансиям
        :return:
        '''
        pass

    def get_vacancies_with_higher_salary(self):
        '''
        Функция получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        :return:
        '''
        pass

    def get_vacancies_with_keyword(self):
        '''
        Функция получает список всех вакансий, в названии которых содержатся переданные в метод слова
        :return:
        '''
        pass
