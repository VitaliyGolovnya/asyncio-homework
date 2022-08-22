import asyncio
import aiohttp
import datetime
from more_itertools import chunked
import psycopg2
from psycopg2 import Error

MAX_CHUNK = 30



async def get_people(session, people_id):
        async with session.get(f'https://swapi.dev/api/people/{people_id}') as response:
            json_data = await response.json()
            await add_to_db(json_data)
            return json_data

async def add_to_db(json_data):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="admin",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="swapi_db")
        cursor = connection.cursor()
        insert_query = '''INSERT INTO people 
                       VALUES(
                       %(birth_year)s, 
                       %(eye_color)s, 
                       %(films)s, 
                       %(gender)s, 
                       %(hair_color)s, 
                       %(height)s, 
                       %(homeworld)s, 
                       %(mass)s, 
                       %(name)s, 
                       %(skin_color)s, 
                       %(species)s, 
                       %(starships)s, 
                       %(vehicles)s);'''
        cursor.execute(insert_query, json_data)
        connection.commit()
        print("Запись успешно вставлена")
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

async def main():

    async with aiohttp.ClientSession() as session:
        coroutines = [get_people(session, i) for i in range(1, 100)]
        for coroutines_chunk in chunked(coroutines, MAX_CHUNK):
            result = await asyncio.gather(*coroutines_chunk)
            for item in result:
                print(item)

asyncio.get_event_loop().run_until_complete(main())