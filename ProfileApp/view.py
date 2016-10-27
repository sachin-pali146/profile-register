#!/usr/bin/python

import os
import cgi
from model import Employee
import mysql.connector
from mysql.connector import Error


def execute(query):
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='profiledb',
                                       user='root',
                                       password='mindfire')
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
    dict_fields = get_formvalues()
    e = Employee(dict_fields)
    insert_query = e.insert()

    print("Content-type:text/html\r\n\r\n")
    print(dict_fields)
    # execute(insert_query)