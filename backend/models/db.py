import psycopg2
from psycopg2.extras import RealDictCursor
from config.config import Config
import os

class DBWrapper:
    def __init__(self, conn):
        self._conn = conn

    def execute(self, query, params=()):
        cur = self._conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, params)
        return cur

    def commit(self):
        self._conn.commit()

    def close(self):
        self._conn.close()

def get_db_connection():
    conn = psycopg2.connect(Config.SUPABASE_URI)
    return DBWrapper(conn)

def init_db():
    conn = psycopg2.connect(Config.SUPABASE_URI)
    cur = conn.cursor()
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    with open(schema_path, 'r') as f:
        schema = f.read()
    cur.execute(schema)
    conn.commit()
    cur.close()
    conn.close()
