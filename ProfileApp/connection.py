#!/usr/bin/python3
"""
Creates connection with database and run SQL queries.
"""
import configparser

import mysql.connector
from mysql.connector import Error

from utils import create_log


def connect():
    """
    Creates mysql connection object
    :return: connection object
    """
    try:
        config = configparser.ConfigParser()
        config.read('constants.cnf')
        conn = mysql.connector.connect(host=config.get('client', 'host'), database=config.get('client', 'database'),
                                       user=config.get('client', 'user'),
                                       password=config.get('client', 'password'))
        return conn
    except Error as e:
        create_log("Connection.py : connect : " + str(e))


def execute(query):
    """
    This function is used for creating the connection with database and executing the queries.
    :param query: array having mysql query to be executed and values for the query
    :return: dictionary having mysql cursor, last row id and all the records.
    """
    try:
        conn = connect()
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True, buffered=True)
            cursor.execute(query[0], query[1])
            output = dict()
            if 'SELECT' in cursor.statement:
                output["fetchall"] = cursor.fetchall()
            output["lastrowid"] = cursor.lastrowid
            output["cursor"] = cursor
            conn.commit()
            return output

    except Error as e:
        create_log("Connection.py : execute : " + str(e))
    finally:
        conn.close()


def login(email_id):
    """
    Function is used to get user id and password details
    :param email_id: email id of user
    :return: dictionary having user id and password.
    """

    result = ''
    try:
        conn = connect()
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True, buffered=True)
            cursor.execute("SELECT id,password,active FROM employee WHERE email=%s", (email_id,))
            result = cursor.fetchone()
            return result
    except Error as e:
        create_log("Connection.py : login : " + str(e))
    finally:
        conn.close()


def public_profile(query):
    """
    Function is used to get all the public profiles
    :param query: SQL query for the public profiles
    :return: dictionary having total count and limited users details according to offset.
    """
    try:
        conn = connect()
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True, buffered=True)
            cursor.execute(query[0], query[1])
            output = dict()
            output["fetchall"] = cursor.fetchall()
            cursor.execute("SELECT FOUND_ROWS()")
            output["total"] = cursor.fetchone()["FOUND_ROWS()"]
            conn.commit()
            return output
    except Error as e:
        create_log("Connection.py : public_profile : " + str(e))
    finally:
        conn.close()


def activate(email_id):
    """
    Function is used to activate profile of new users
    :param email_id: email id of user
    :return: lastrowid
    """

    result = ''
    try:
        conn = connect()
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True, buffered=True)
            cursor.execute("UPDATE employee SET active = TRUE WHERE email = %s", (email_id,))
            result = cursor.lastrowid
            conn.commit()
            return result
    except Error as e:
        create_log("Connection.py : activate : " + str(e))

    finally:
        conn.close()
