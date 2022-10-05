import sqlite3 as sql
import numpy as np
import io
from core.consts import DATABASE

def create():
    con = sql.connect(DATABASE, isolation_level=None)
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE encoding ( id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL, encoding BLOB NOT NULL );"
    )
    con.commit()


def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sql.Binary(out.read())


def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)

def insert_array (user_id, encoding):
    blob = adapt_array(encoding)

    con = sql.connect(DATABASE, isolation_level=None)
    cur = con.cursor()
    cur.execute("INSERT INTO encoding (user_id, encoding) VALUES (?, ?)", (user_id, blob))
    con.commit()