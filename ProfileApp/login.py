#!/usr/bin/python3

import cgi
import cgitb
from connection import execute,login
import os

cgitb.enable()
form = cgi.FieldStorage()
if os.environ['REQUEST_METHOD'] == 'GET':
    print("Content-type: text/html")
    print('')
    f = open('./template/login.html')
    print(f.read())
    f.close()
elif os.environ['REQUEST_METHOD'] == 'POST':
    print("Content-type:text/html\r\n\r\n")
    form_email = form.getvalue('email')
    form_password = form.getvalue('password')
    password_db = login(form_email)
    # print(password_db)
    if password_db:
        if password_db == form_password:
            print('You are logged in.')
        else:
            print('Check the password')
    else:
        print('Check the username')