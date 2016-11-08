#!/usr/bin/python3
import cgi
import cgitb
import os

from session import delete_cookie

cgitb.enable()
form = cgi.FieldStorage()
if os.environ['REQUEST_METHOD'] == 'GET':
    logout = delete_cookie()
    if logout:
        print(logout)
    print("Location: http://localhost/login.py\n")