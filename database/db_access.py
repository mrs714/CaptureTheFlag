from database.db_consts import *
import sqlite3
import json

class _DBManager:
    def __init__(self):
        self._path = DATABASE_PATH
        self._conn = None
        self._cursor = None

    def __enter__(self):
        self._conn = sqlite3.connect(self._path)
        self._conn.row_factory = sqlite3.Row
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
    config = {"health": 100, "shield": 100, "attack": 100}
    config_string = json.dumps(config)
    with _db as db:
        c = db.get_cursor()
        c.execute(f"INSERT INTO {DATABASE_USER_TABLE} VALUES (null, ?, ?, null, null, null, null, 0, ?)", (username, password, config_string))
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
    
def get_user_id(username):
    with _db as db:
        c = db.get_cursor()
        c.execute(f"SELECT id FROM {DATABASE_USER_TABLE} WHERE username = ?", (username,))
        return c.fetchone()[0]

def save_code(id, code):
    with _db as db:
        c = db.get_cursor()
        c.execute(f"UPDATE {DATABASE_USER_TABLE} SET code = ?, is_executable = 1 WHERE id = ?", (code, id))

def save_config(id, config):
    with _db as db:
        c = db.get_cursor()
        c.execute(f"UPDATE {DATABASE_USER_TABLE} SET config = ? WHERE id = ?", (config, id))

def get_config(id):
    with _db as db:
        c = db.get_cursor()
        c.execute(f"SELECT config FROM {DATABASE_USER_TABLE} WHERE id = ?", (id,))
        return c.fetchone()[0]
    
def get_code(id):
    with _db as db:
        c = db.get_cursor()
        c.execute(f"SELECT code FROM {DATABASE_USER_TABLE} WHERE id = ?", (id,))
        return c.fetchone()[0]

def get_bots_to_execute():
    with _db as db:
        c = db.get_cursor()
        c.execute(f"SELECT id, username, code, config FROM {DATABASE_USER_TABLE} WHERE is_executable = 1")
        return c.fetchall()

def get_info(id):
    with _db as db:
        c = db.get_cursor()
        c.execute(f"SELECT last_position, date_last_execution FROM {DATABASE_USER_TABLE} WHERE id = ?", (id,))
        info = c.fetchone()
        return info[0], info[1]

def get_error(id):
    with _db as db:
        c = db.get_cursor()
        c.execute(f"SELECT last_execution_result FROM {DATABASE_USER_TABLE} WHERE id = ?", (id,))
        return c.fetchone()[0]
def update_info(id, last_position, date_last_execution, last_execution_result, is_executable):

    with _db as db:
        c = db.get_cursor()
        c.execute(f"UPDATE {DATABASE_USER_TABLE} SET last_position = ?, date_last_execution = ?, last_execution_result = ?, is_executable = ? WHERE id = ?", (last_position, date_last_execution, last_execution_result, is_executable, id))

        