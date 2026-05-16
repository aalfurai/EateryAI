import os
import psycopg2.pool
from dotenv import load_dotenv

load_dotenv()

db_pool = None

def init_pool():
    global db_pool
    db_pool = psycopg2.pool.ThreadedConnectionPool(
        minconn=2,
        maxconn=10,
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )

def get_db():
    conn = db_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("SET search_path TO eateryai_test1, public;")
            conn.commit()
        yield conn
    finally:
        db_pool.putconn(conn)