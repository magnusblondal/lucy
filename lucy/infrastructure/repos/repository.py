import psycopg2
import psycopg2.extras
import psycopg2.sql
import psycopg2.pool

from config import settings


class Repository:
    def __init__(self):
        self.pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            host=settings.db_host,
            port=settings.db_port,
            database=settings.db_name,
            user=settings.db_user,
            password=settings.db_pass
        )

    def _execute(self, sql: str, values):
        connection = self.pool.getconn()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute(sql, values)
        connection.commit()
        cursor.close()
        connection.close()

    def _fetch_one(self, sql: str, values):
        connection = self.pool.getconn()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result

    def _fetch_all(self, sql: str, values=None):
        connection = self.pool.getconn()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute(sql, values)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result
