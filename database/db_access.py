from database.db_consts import *
import sqlite3

class _DBManager:
    def __init__(self):
        self._path = DATABASE_PATH
        self._conn = None
        self._cursor = None

    def __enter__(self):
        self._conn = sqlite3.connect(self._path)
        self._cursor = self._conn.cursor()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.save()
        else:
            self._conn.rollback()
        self._cursor.close()
        self._conn.close()
        self._cursor = None
        self._conn = None
    
    def save(self):
        self._conn.commit()
    
    def get_cursor(self):
        return self._cursor

    
_db = _DBManager()

def insert_user(username, password):
    with _db as db:
        c = db.get_cursor()
        c.execute(f"INSERT INTO {DATABASE_USER_TABLE} VALUES (null, ?, ?, null, null, null, null, 1)", (username, password))
        return c.lastrowid

def exists_user(username):
    with _db as db:
        c = db.get_cursor()
        c.execute(f"SELECT * FROM {DATABASE_USER_TABLE} WHERE username = ?", (username,))
        return c.fetchone() is not None

def check_user_credentials(username, password):
    with _db as db:
        c = db.get_cursor()
        c.execute(f"SELECT * FROM {DATABASE_USER_TABLE} WHERE username = ? AND password = ?", (username, password))
        return c.fetchone() is not None