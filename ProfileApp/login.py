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
from utils import create_log, show_404, generate_hash, Csrf

try:
    config = configparser.ConfigParser()
    config.read('constants.cnf')
    cgitb.enable()
    form = cgi.FieldStorage()
    session = Session()
    current_user = session.current_user()
    token = Csrf()
    form_csrf = dict()
    form_csrf["csrf"] = token.generate()
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
            print(f.read() % form_csrf)
            f.close()
            f = open('./template/footer.html', encoding="utf_8")
            print(f.read() % footer)
            f.close()
    elif os.environ['REQUEST_METHOD'] == 'POST':
        form_email = form.getvalue('email')
        form_password = form.getvalue('password')
        user = login(form_email)
        if "csrfToken" in form.keys():
            form_token = form.getvalue("csrfToken")
        else:
            form_token = ''

        if token.validate_token(form_token):
            if user:
                if user["password"] == generate_hash(form_password):
                    session.session(user)
                else:
                    print("Location: http://localhost/edit_profile.py\n")
                    print('Check the password')
            else:
                print("Location: http://localhost/edit_profile.py\n")
                print('Check the username')
        else:
            create_log("Login.py : Someone Tried CSRF")
            print("Location: http://localhost/login.py\n")
except Exception as e:
    create_log("Login.py : " + str(e))
    show_404()
