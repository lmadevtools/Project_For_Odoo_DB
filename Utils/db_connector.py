import psycopg2

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from Utils.queries import *

class DBConnector:
    def __init__(self):
        self._connection = None
        self._cursor    = None


    def connect(self):
        try:
            self._connection = psycopg2.connect(
                dbname      = DB_NAME,
                host        = DB_HOST,
                port        = DB_PORT,
                user        = DB_USER,
                password    = DB_PASSWORD
            )
            self._cursor = self._connection.cursor()
        except Exception as e:
            print(f"Error: {e}")

    def disconnect(self):
        if self._cursor:
            self._cursor.close()
        if self._connection:
            self._connection.close()

    def execute(self, query, params=None):
        self._cursor.execute(query, params)
        return self._cursor
    
    def commit(self):
        self._connection.commit()
