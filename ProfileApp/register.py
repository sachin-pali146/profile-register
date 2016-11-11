#!/usr/bin/python3
"""
Create register page for new users and save their data in database.
"""

import configparser
import os

from connection import execute
from model import Employee
from utils import create_log, get_formvalues, save_uploaded_file, send_email, show_404, Csrf

try:
    config = configparser.ConfigParser()
    config.read('constants.cnf')
    token = Csrf()
    form = dict()
    form["csrf"] = token.generate()
    header = dict()
    header["title"] = "Register"
    header["homeUrl"] = "http://localhost/register.py"
    header["navTopRight"] = '<li class="active"><a href="http://localhost/login.py">Login</a></li>'
    header["css_version"] = config.get("version", "css")
    footer = {
        "js_version": config.get("version", "css")
    }
    if os.environ['REQUEST_METHOD'] == 'GET':
        print("Content-type: text/html\n")
        f = open('./template/header.html')
        print(f.read() % header)
        f.close()
        f = open('./template/register.html')
        print(f.read() % form)
        f.close()
        f = open('./template/footer.html')
        print(f.read() % footer)
        f.close()
    elif os.environ['REQUEST_METHOD'] == 'POST':
        dict_fields = get_formvalues()
        if "csrfToken" in dict_fields.keys():
            form_token = dict_fields["csrfToken"]
        else:
            form_token = ''
        if token.validate_token(form_token):
            e = Employee(dict_fields)
            insert_query = e.insert_employee()
            activation = e.activation()
            last_id = execute(insert_query)["lastrowid"]
            if dict_fields['photo'].filename:
                image_ext = dict_fields['photo'].filename.split('.')[-1]
                image_name = str(last_id) + '.' + image_ext
                image_query = e.set_image(image_ext, str(last_id))
                execute(image_query)
                save_uploaded_file(dict_fields['photo'], config.get('profile', 'path'), image_name)
            print("Content-type:text/html\r\n\r\n")
            print("Please click on activation link sent in email in order to complete registration process.")
            send_email(dict_fields["email"], activation)
        else:
            create_log("Register.py : Someone Tried CSRF")
            print("Location: http://localhost/register.py\n")
except Exception as e:
    create_log("Register.py : " + str(e))
    show_404()
