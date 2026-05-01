import os
import psycopg2
from dotenv import load_dotenv

# Only connects to local databases (ie. your desktop PostgreSQL server only)
class EateryDatabaseConnection:
    def __init__(self, dbname = None, user = None, pw = None, host= None, port = None):
        load_dotenv()
        self.__dbname = dbname if dbname else os.getenv("DB_NAME")
        self.__user = user if user else os.getenv("DB_USER")
        self.__pw = pw if pw else os.getenv("DB_PASSWORD")
        self.__host = host if host else os.getenv("DB_HOST")
        self.__port = port if port else os.getenv("DB_PORT")
        self.__conn = None
    
    def __enter__(self):
        self.__conn = self.__establish_connection()
        return self.__conn
        
    def __del__(self):
        if hasattr(self, '_EateryDatabaseConnection__conn') and self.__conn:
            self.__conn.close()
            self.__conn = None
            print("Database closed through __del__")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__conn:
            self.__conn.close()
            self.__conn = None
            print("Connection closed via Context Manager")

    def __establish_connection(self):
        try:
            conn = psycopg2.connect(
                dbname = self.__dbname,
                user = self.__user,
                password = self.__pw,
                host = self.__host,
                port = self.__port
            )

            with conn.cursor() as cur:
                cur.execute("SET search_path TO eateryai_test1, public;")
                conn.commit()

            print("Successfully connected to the database!")
            return conn

        except Exception as db_exception:
            print(f"Failed to connection: {db_exception}")
            return None


# if __name__ == "__main__":
#     eat = EateryDatabaseConnection()
#     with eat as es:
#         print("hi i just made a connection")