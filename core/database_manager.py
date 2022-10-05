import sqlite3 as sql
import numpy as np
import io
from core.consts import DATABASE


def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sql.Binary(out.read())


def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)


def get_database():
    sql.register_adapter(np.ndarray, adapt_array)

    sql.register_converter("array", convert_array)

    con = sql.connect(DATABASE, isolation_level=None, detect_types=sql.PARSE_DECLTYPES)

    return con


def create_database():
    con = get_database()
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE encoding ( id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, encoding BLOB NOT NULL );"
    )
    con.commit()


def insert_array(user_id, encoding):
    blob = adapt_array(encoding)

    con = get_database()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO encoding (user_id, encoding) VALUES (?, ?)", (user_id, blob)
    )
    con.commit()


def get_array(user_id):
    con = get_database()
    cur = con.cursor()
    cur.execute("SELECT encoding FROM encoding WHERE user_id = ?", (user_id,))
    return [convert_array(blob[0]) for blob in cur.fetchall()]


def get_all():
    con = get_database()
    cur = con.cursor()
    cur.execute("SELECT * FROM encoding")

    return cur.fetchall()
