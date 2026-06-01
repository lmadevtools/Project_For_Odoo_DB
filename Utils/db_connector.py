import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from Utils.queries import *

DB_CONFIG = {
"host": DB_HOST,
"port": DB_PORT,
"database": DB_NAME, 
"user": DB_USER,
"password" : DB_PASSWORD
}

class DBConnector:
    def __init__(self):
        self._connection = None
        self._cursor    = None

    def _get_connection(self,DB_CONFIG):
        return psycopg2.connect(**DB_CONFIG)  #each key of the dict is a param

    def connect(self):
        try:
            self._connection = self._get_connection(DB_CONFIG)
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


#pyodbc
#sqlalchimy