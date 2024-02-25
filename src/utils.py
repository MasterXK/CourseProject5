import psycopg2
import dotenv
import os
from config import config
from HHParser import HHParser

dotenv.load_dotenv()
PSQL_PASS = os.getenv('PSQL_PASS')


def create_database(db_name):
    conn_params = dict(
        host="localhost",
        database="postgres",
        user="postgres",
        password=PSQL_PASS
    )

    conn = psycopg2.connect(dbname='postgres', **config())
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f'DROP DATABASE IF EXISTS {db_name}')
    cur.execute(f'CREATE DATABASE {db_name}')

    cur.close()
    conn.close()


def create_tables(db_name):
    conn = psycopg2.connect(dbname=db_name, **config())
    with conn:
        with conn.cursor() as cur:
            cur.execute('CREATE TABLE employers'
                        '(id int PRIMARY KEY,'
                        'name varchar(255) UNIQUE NOT NULL)')

            cur.execute('CREATE TABLE vacancies'
                        '(id int PRIMARY KEY,'
                        'name varchar(255) NOT NULL,'
                        'area varchar(255),'
                        'salary_from int,'
                        'salary_to int,'
                        'url varchar(255),'
                        'published_at timestamp,'
                        'employer int REFERENCES employers(id) NOT NULL)')
    conn.close()


def inset_data(db_name):
    conn = psycopg2.connect(dbname=db_name, **config())
    with conn:
        with conn.cursor() as cur:
            cur.execute('CREATE TABLE employers'
                        '(id int PRIMARY KEY,'
                        'name varchar(255) UNIQUE NOT NULL)')

            cur.execute('CREATE TABLE vacancies'
                        '(id int PRIMARY KEY,'
                        'name varchar(255) NOT NULL,'
                        'area varchar(255),'
                        'salary_from int,'
                        'salary_to int,'
                        'url varchar(255),'
                        'published_at timestamp,'
                        'employer int REFERENCES employers(id) NOT NULL)')
    conn.close()


def insert_data(db_name):
    hh = HHParser()
    employers = hh.get_employers()
    vacancies = hh.get_all_vacancies()
    conn = psycopg2.connect(dbname=db_name, **config())
    with conn:
        with conn.cursor() as cur:
            for employer in employers:
                cur.execute('INSERT INTO employers VALUES (%s, %s)'
                            'ON CONFLICT (id) DO NOTHING',
                            (employer['id'], employer['name']))

            for vacancy in vacancies:
                cur.execute('INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
                            'ON CONFLICT (id) DO NOTHING',
                            (vacancy['id'], vacancy['name'],
                             vacancy['area'], vacancy['salary_from'],
                             vacancy['salary_to'], vacancy['url'],
                             vacancy['published_at'], vacancy['employer']
                             ))
    conn.close()


if __name__ == '__main__':
    create_database('course_work_5')
    create_tables('course_work_5')
    insert_data('course_work_5')
