#!/usr/bin/python3

import os
import cgi
from model import Employee
import mysql.connector
from mysql.connector import Error


def execute(query):
    """
    This function is used for creating the connection with database and executing the queries.

    """

    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='profiledb',
                                       user='root',
                                       password='mindfire')
        print('hello')
        print(query)
        if conn.is_connected():
            print('Connected to MySQL database')
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()

    except Error as e:
        print(e)

    finally:
        conn.close()


def get_formvalues():
    """
    This function is used to create dictionary for all the fields on Form.
    """
    form = cgi.FieldStorage()
    dict_fields = {}
    for i in form:
        dict_fields[str(i)] = form.getvalue(str(i))
    return dict_fields


if os.environ['REQUEST_METHOD'] == 'GET':
    print("Content-type: text/html")
    print('')
    f = open('./template/index.html')
    print(f.read())
    f.close()
elif os.environ['REQUEST_METHOD'] == 'POST':
    print("Content-type:text/html\r\n\r\n")
    dict_fields = get_formvalues()
    e = Employee(dict_fields)
    insert_query = e.insert()


    print(dict_fields)
    execute(insert_query)