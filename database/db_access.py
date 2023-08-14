from database.db_consts import *
import sqlite3
import json
import log

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
    try:
        config = {"health": 100, "shield": 100, "attack": 100}
        config_string = json.dumps(config)
        with _db as db:
            c = db.get_cursor()
            c.execute(f"INSERT INTO {DATABASE_USER_TABLE} VALUES (null, ?, ?, null, null, null, null, 0, ?)", (username, password, config_string))
            return c.lastrowid
    except Exception as e:
        log.e(f"Error inserting user {username} in the database: {e}")

def exists_user(username):
    try:
        with _db as db:
            c = db.get_cursor()
            c.execute(f"SELECT * FROM {DATABASE_USER_TABLE} WHERE username = ?", (username,))
            return c.fetchone() is not None
    except Exception as e:
        log.e(f"Error checking if user {username} exists in the database: {e}")

def check_user_credentials(username, password):
    try:
        with _db as db:
            c = db.get_cursor()
            c.execute(f"SELECT * FROM {DATABASE_USER_TABLE} WHERE username = ? AND password = ?", (username, password))
            return c.fetchone() is not None
    except Exception as e:
        log.e(f"Error checking user {username} credentials in the database: {e}")
    
def get_user_id(username):
    try:
        with _db as db:
            c = db.get_cursor()
            c.execute(f"SELECT id FROM {DATABASE_USER_TABLE} WHERE username = ?", (username,))
            return c.fetchone()[0]
    except Exception as e:
        log.e(f"Error getting user {username} id from the database: {e}")

def save_code(id, code):
    try:
        with _db as db:
            c = db.get_cursor()
            c.execute(f"UPDATE {DATABASE_USER_TABLE} SET code = ?, is_executable = 1 WHERE id = ?", (code, id))
    except Exception as e:
        log.e(f"Error saving code for user {id} in the database: {e}")

def save_config(id, config):
    try:
        with _db as db:
            c = db.get_cursor()
            c.execute(f"UPDATE {DATABASE_USER_TABLE} SET config = ? WHERE id = ?", (config, id))
    except Exception as e:
        log.e(f"Error saving config for user {id} in the database: {e}")

def get_config(id):
    try:
        with _db as db:
            c = db.get_cursor()
            c.execute(f"SELECT config FROM {DATABASE_USER_TABLE} WHERE id = ?", (id,))
            return c.fetchone()[0]
    except Exception as e:
        log.e(f"Error getting config for user {id} from the database: {e}")
    
def get_code(id):
    try:
        with _db as db:
            c = db.get_cursor()
            c.execute(f"SELECT code FROM {DATABASE_USER_TABLE} WHERE id = ?", (id,))
            return c.fetchone()[0]
    except Exception as e:
        log.e(f"Error getting code for user {id} from the database: {e}")

def get_bots_to_execute():
    try:
        with _db as db:
            c = db.get_cursor()
            c.execute(f"SELECT id, username, code, config FROM {DATABASE_USER_TABLE} WHERE is_executable = 1")
            return c.fetchall()
    except Exception as e:
        log.e(f"Error getting bots to execute from the database: {e}")

def get_info(id):
    try:
        with _db as db:
            c = db.get_cursor()
            c.execute(f"SELECT last_position, date_last_execution FROM {DATABASE_USER_TABLE} WHERE id = ?", (id,))
            temp = c.fetchone()
            return temp[0], temp[1]
    except Exception as e:
        log.e(f"Error getting info for user {id} from the database: {e}")

def get_error(id):
    try:
        with _db as db:
            c = db.get_cursor()
            c.execute(f"SELECT last_execution_result FROM {DATABASE_USER_TABLE} WHERE id = ?", (id,))
            return c.fetchone()[0]
    except Exception as e:
        log.e(f"Error getting error for user {id} from the database: {e}")

def update_info(id, last_position, date_last_execution, last_execution_result, is_executable):
    try:
        with _db as db:
            c = db.get_cursor()
            c.execute(f"UPDATE {DATABASE_USER_TABLE} SET last_position = ?, date_last_execution = ?, last_execution_result = ?, is_executable = ? WHERE id = ?", (last_position, date_last_execution, last_execution_result, is_executable, id))
    except Exception as e:
        log.e(f"Error updating info for user {id} in the database: {e}")
        