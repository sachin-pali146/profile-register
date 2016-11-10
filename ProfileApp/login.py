#!/usr/bin/python3
"""
Create login page and check the login credentials and redirect users to appropriate page.
"""
import cgi
import cgitb
import configparser
import os

from connection import login
from session import Session

config = configparser.ConfigParser()
config.read('constants.cnf')
cgitb.enable()
form = cgi.FieldStorage()
session = Session()
current_user = session.current_user()
header = dict()
header["title"] = "Login"
header["homeUrl"] = "http://localhost/register.py"
header["navTopRight"] = '<li class="active"><a href="http://localhost/register.py">Register Now</a></li>'
header["css_version"] = config.get("version", "css")
footer = {
    "js_version": config.get("version", "css")
}
if os.environ['REQUEST_METHOD'] == 'GET':
    if current_user:
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
        print(f.read() % footer)
        f.close()
elif os.environ['REQUEST_METHOD'] == 'POST':
    form_email = form.getvalue('email')
    form_password = form.getvalue('password')
    user = login(form_email)

    if user:
        if user["password"] == form_password:
            session.session(user)
        else:
            print("Location: http://localhost/edit_profile.py\n")
            print('Check the password')
    else:
        print("Location: http://localhost/edit_profile.py\n")
        print('Check the username')
