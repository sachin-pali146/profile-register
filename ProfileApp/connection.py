#!/usr/bin/python3

import mysql.connector
from mysql.connector import Error


def connect():
    conn = mysql.connector.connect(host='localhost',
                                       database='profiledb',
                                       user='root',
                                       password='mindfire')
    return conn
def execute(query):
    """
    This function is used for creating the connection with database and executing the queries.

    """

    try:
        conn = connect()

        if conn.is_connected():
            # print('Connected to MySQL database')
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()

    except Error as e:
        print(e)

    finally:
        conn.close()
        return cursor.lastrowid


def login(emailid):
    password_db = ''
    try:
        conn = connect()
        if conn.is_connected():
            cursor = conn.cursor(buffered=True)
            # emailid1='sachin.pali@daf.com'
            # cursor.execute("SELECT password from employee where email=%s", (emailid1,))
            # print(cursor.fetchone())
            cursor.execute("SELECT password from employee where email=%s", (emailid,))
            password_db = cursor.fetchone()[0]
            # print(cursor.fetchone())

    except Error as e:
        print(e)

    finally:
        conn.close()
        return password_db