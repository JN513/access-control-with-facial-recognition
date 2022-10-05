from operator import imod
import sqlite3 as sql
import numpy as np
import io


def create():
    con = sql.connect("database.bd", isolation_level=None)
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
