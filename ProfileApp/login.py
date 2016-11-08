#!/usr/bin/python3

import cgi
import cgitb
import os

from session import session, current_user
from connection import login


cgitb.enable()
form = cgi.FieldStorage()
header = dict()
header["title"] = "Login"
header["homeUrl"] = "http://localhost/register.py"
header["navTopRight"] = '<li class="active"><a href="http://localhost/register.py">Register Now</a></li>'
if os.environ['REQUEST_METHOD'] == 'GET':
    if current_user():
        print("Location: http://localhost/edit_profile.py\n")
    else:
        print("Content-type: text/html\n")
        f = open('./template/header.html', encoding='utf-8')
        print(f.read() % header)
        f.close()
        f = open('./template/login.html')
        print(f.read())
        f.close()
        f = open('./template/footer.html', encoding="utf_8")
        print(f.read())
        f.close()
elif os.environ['REQUEST_METHOD'] == 'POST':
    form_email = form.getvalue('email')
    form_password = form.getvalue('password')
    user = login(form_email)
    if user:
        if user["password"] == form_password:
            session(user)
        else:
            print("Location: http://localhost/edit_profile.py\n")
            print('Check the password')
    else:
        print("Location: http://localhost/edit_profile.py\n")
        print('Check the username')