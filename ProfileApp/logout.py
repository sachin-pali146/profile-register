#!/usr/bin/python3
"""
Logout the current user and redirect them to login page
"""
import cgi
import cgitb
import os

from session import Session

cgitb.enable()
form = cgi.FieldStorage()
session = Session()
user = session.current_user()

if user:
    if os.environ['REQUEST_METHOD'] == 'GET':
        logout = session.delete_cookie()
        if logout:
            print(logout)
        print("Location: http://localhost/login.py\n")
else:
    print("Location: http://localhost/login.py\n")
