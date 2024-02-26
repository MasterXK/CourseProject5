from src.DBManager import DBManager
from src.HHParser import HHParser
from src.utils import create_database, create_tables, insert_data


def main():
    hh = HHParser()

    db_name = input('Enter database name to create: ')

    create_database(db_name)
    create_tables(db_name)

    companies_number = input('How much companies to investigate? ')
    vacancies_per_company = input('Number of vacancies per company: ')

    employers = hh.get_employers({'per_page': companies_number})
    vacancies = hh.sort_vacancies(hh.get_all_vacancies(employers, {'per_page': vacancies_per_company}))

    insert_data(db_name, employers, vacancies)

    db_mngr = DBManager(db_name)
    companies_and_vacancies_count = db_mngr.get_companies_and_vacancies_count()
    print('Кол-во компаний', companies_and_vacancies_count[0], '\n',
          'Кол-во компаний', companies_and_vacancies_count[0], '\n',
          'Кол-во компаний', db_mngr.get_avg_salary())

    while True:
        try:
            to_do = int(input('Выберите действие:\n'
                              '1 - Показать вакансии с зарплатой, выше среднего.\n'
                              '2 - Вывести вакансии по ключевому слову в названии.\n'
                              '3 - Выход.'))

        except ValueError:
            to_do = int(input('Введите число:\n'
                              '1 - Показать вакансии с зарплатой, выше среднего.\n'
                              '2 - Вывести вакансии по ключевому слову в названии.\n'
                              '3 - Выход.\n'))

        if to_do == 1:
            vacancies = db_mngr.get_vacancies_with_higher_salary()

        elif to_do == 2:
            keywords = input('Введите ключевое слово или слова: ')
            vacancies = db_mngr.get_vacancies_with_keyword(keywords)

        else:
            break

        print('id', '\t|', 'name', '\t|',
              'area', '\t|', 'salary_from', '\t|',
              'salary_to', '\t|', 'url', '\t|',
              'published_at', '\t|', 'employer')
        for vacancy in vacancies:
            print('\t|'.join([str(data) if not type(data) is str else data for data in vacancy]))


if __name__ == '__main__':
    main()
