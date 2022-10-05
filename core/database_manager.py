import sqlite3 as sql
import numpy as np
import io
import os
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
        "CREATE TABLE encoding ( id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, encoding BLOB NOT NULL, Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP );"
    )
    cur.execute(
        "CREATE TABLE data_alter ( id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP );"
    )
    cur.execute(
        "CREATE TABLE user_acess ( id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL UNIQUE, Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP );"
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


def insert_data_alter(user_id):
    con = get_database()
    cur = con.cursor()
    cur.execute("INSERT INTO data_alter (user_id) VALUES (?)", (user_id,))
    con.commit()


def insert_user_acess(user_id):
    con = get_database()
    cur = con.cursor()
    cur.execute("INSERT INTO user_acess (user_id) VALUES (?)", (user_id,))
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

    users = []
    encodings = []

    for result in cur.fetchall():
        users.append(result[1])
        encodings.append(convert_array(result[2]))

    return users, encodings


def get_data_alter():
    con = get_database()
    cur = con.cursor()
    cur.execute("SELECT * FROM data_alter")

    result = cur.fetchall()

    return result


def delete_from_user(user_id):
    con = get_database()
    cur = con.cursor()
    cur.execute("DELETE FROM encoding WHERE user_id = ?", (user_id,))
    con.commit()


def delete_all():
    con = get_database()
    cur = con.cursor()
    cur.execute("DELETE FROM encoding WHERE 1")
    con.commit()


def count_user_encoding(user_id):
    con = get_database()
    cur = con.cursor()
    cur.execute("SELECT COUNT(id) FROM encoding WHERE user_id = ?", (user_id,))

    return cur.fetchone()[0]
