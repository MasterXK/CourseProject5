import psycopg2
import dotenv
import os


dotenv.load_dotenv()
PSQL_PASS = os.getenv('PSQL_PASS')
CSV_TO_INPUT = os.listdir("north_data")


def main():
    conn_params = dict(
        host="localhost",
        database="north",
        user="postgres",
        password=PSQL_PASS
    )

    with psycopg2.connect(**conn_params) as conn:
        for file in CSV_TO_INPUT:
            with open(os.path.join('north_data', file), encoding='UTF-8') as f:
                reader = csv.reader(f)
                headers = next(reader)
                values = [tuple([value.strip(r'"') for value in data]) for data in reader]
                print(values)
                with conn.cursor() as cur:
                    cur.executemany(f"INSERT INTO {file[:-9]} VALUES ({'%s' + ', %s' * (len(headers) - 1)})", values)

        conn.commit()


if __name__ == '__main__':
    main()
