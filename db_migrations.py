import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_db():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="admin",
                                      host="127.0.0.1",
                                      port="5432")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        sql_create_database = 'CREATE DATABASE swapi_db'
        cursor.execute(sql_create_database)
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

def create_table():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="admin",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="swapi_db")

        cursor = connection.cursor()

        create_table_query = '''CREATE TABLE IF NOT EXISTS people
                              (birth_year TEXT,
                              eye_color TEXT,
                              films TEXT,
                              gender TEXT,
                              hair_color TEXT,
                              height TEXT,
                              homeworld TEXT,
                              mass TEXT,
                              name TEXT PRIMARY KEY,
                              skin_color TEXT,
                              species TEXT,
                              starships TEXT,
                              vehicles TEXT); '''

        cursor.execute(create_table_query)
        connection.commit()
        print("Таблица успешно создана в PostgreSQL")

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")
create_db()
create_table()