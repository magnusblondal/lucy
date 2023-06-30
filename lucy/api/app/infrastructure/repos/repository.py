from pydantic import BaseModel
import psycopg2
import psycopg2.extras
import psycopg2.sql

DB_HOST = '127.0.0.1'
DB_PORT = 5432
DB_NAME = 'trdr_kraken'
DB_USER = 'trdr'
DB_PASS = 'secret'

class Repository:
    def test(self):
        connection = psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        mSql = '''
            INSERT INTO bots
            (id, name, description, active, capital, entry_size, so_size, max_safety_orders, allow_shorts)
            VALUES
            ('botId_2', 'Bot 2', 'Bot 2 description', true, 1000, 10, 10, 10, false)
            '''
        cursor.execute(mSql)
        connection.commit()
        cursor.close()
        connection.close()

    def _execute(self, sql: str, values):
        connection = psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute(sql, values)
        connection.commit()
        cursor.close()
        connection.close()

    def _fetch_one(self, sql: str, values):
        connection = psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result
    
    def _fetch_all(self, sql: str, values= None):
        connection = psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute(sql, values)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result
    