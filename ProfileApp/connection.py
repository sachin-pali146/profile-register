#!/usr/bin/python3

import mysql.connector
from mysql.connector import Error



def connect():
    conn = mysql.connector.connect(option_files='constants.cnf')
    return conn


def execute(query):
    """
    This function is used for creating the connection with database and executing the queries.

    """

    try:
        conn = connect()

        if conn.is_connected():
            cursor = conn.cursor(dictionary=True, buffered=True)
            cursor.execute(query[0], query[1])
            output = dict()
            output["fetchone"] = cursor.fetchone()
            output["lastrowid"] = cursor.lastrowid
            output["cursor"] = cursor
            conn.commit()
            return output

    except Error as e:
        print(e)

    finally:
        conn.close()


def login(emailid):
    password_db = ''
    try:
        conn = connect()
        if conn.is_connected():
            cursor = conn.cursor(buffered=True)
            cursor.execute("SELECT password from employee where email=%s", (emailid,))
            password_db = cursor.fetchone()[0]
            return password_db
    except Error as e:
        print(e)

    finally:
        conn.close()


