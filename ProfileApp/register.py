#!/usr/bin/python3

import os
import configparser

from model import Employee
from connection import execute
from utils import get_formvalues, save_uploaded_file, send_email

config = configparser.ConfigParser()
config.read('constants.cnf')
header = dict()
header["title"] = "Register"
header["homeUrl"] = "http://localhost/register.py"
header["navTopRight"] = '<li class="active"><a href="http://localhost/login.py">Login</a></li>'

if os.environ['REQUEST_METHOD'] == 'GET':
    print("Content-type: text/html\n")
    f = open('./template/header.html')
    print(f.read() % header)
    f.close()
    f = open('./template/index.html')
    print(f.read())
    f.close()
    f = open('./template/footer.html')
    print(f.read())
    f.close()
elif os.environ['REQUEST_METHOD'] == 'POST':
    print("Content-type:text/html\r\n\r\n")
    dict_fields = get_formvalues()
    e = Employee(dict_fields)
    insert_query = e.insert_employee()
    activation = e.activation()
    last_id = execute(insert_query)["lastrowid"]
    if dict_fields['photo'].filename:
        image_ext = dict_fields['photo'].filename.split('.')[-1]
        image_name = str(last_id)+'.'+image_ext
        image_query = e.set_image(image_ext, str(last_id))
        execute(image_query)
        save_uploaded_file(dict_fields['photo'], config.get('profile', 'path'), image_name)
    print("Please click on activation link sent in email in order to complete registration process.")
    send_email(dict_fields["email"], activation)

